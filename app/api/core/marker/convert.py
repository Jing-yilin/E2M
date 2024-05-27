from api.core.marker.settings import settings
from typing import List, Dict, Tuple, Optional
from api.core.marker.images.save import images_to_dict
from api.core.marker.images.extract import extract_images
from api.core.marker.cleaners.text import cleanup_text
from api.core.marker.postprocessors.markdown import (
    merge_spans,
    merge_lines,
    get_full_text,
)
from api.core.marker.cleaners.fontstyle import find_bold_italic
from api.core.marker.cleaners.headings import split_heading_blocks
from api.core.marker.cleaners.bullets import replace_bullets
from api.core.marker.cleaners.code import identify_code_blocks, indent_blocks
from api.core.marker.postprocessors.editor import edit_full_text
from api.core.marker.pdf.utils import find_filetype
from api.core.marker.equations.equations import replace_equations
from api.core.marker.cleaners.headers import filter_header_footer, filter_common_titles
from api.core.marker.pdf.extract_text import get_text_blocks
from api.core.marker.ocr.recognition import run_ocr
from api.core.marker.ocr.detection import surya_detection
from api.core.marker.ocr.lang import replace_langs_with_codes, validate_langs
from api.core.marker.layout.order import surya_order, sort_blocks_in_reading_order
from api.core.marker.layout.layout import surya_layout, annotate_block_types
from api.core.marker.debug.data import dump_bbox_debug_data
from api.core.marker.tables.table import format_tables
from api.core.marker.utils import flush_cuda_memory
from PIL import Image
import pypdfium2 as pdfium
import warnings
import logging

warnings.filterwarnings(
    "ignore", category=UserWarning
)  # Filter torch pytree user warnings

logger = logging.getLogger(__name__)


def convert_single_pdf(
    fname: str,
    model_lst: List,
    metadata: Optional[Dict] = None,
    langs: Optional[List[str]] = None,
    batch_multiplier: int = 1,
) -> Tuple[str, Dict[str, Image.Image], Dict]:
    # Set language needed for OCR
    if langs is None:
        langs = [settings.DEFAULT_LANG]

    if metadata:
        langs = metadata.get("languages", langs)

    langs = replace_langs_with_codes(langs)
    validate_langs(langs)

    # Find the filetype
    filetype = find_filetype(fname)

    # Setup output metadata
    out_meta = {
        "languages": langs,
        "filetype": filetype,
    }

    if filetype == "other":  # We can't process this file
        return "", out_meta

    # Get initial text blocks from the pdf
    doc = pdfium.PdfDocument(fname)

    total_pages = len(doc)
    logger.info(f"Total pages in document: {total_pages}")

    pages, toc = get_text_blocks(doc)
    out_meta.update(
        {
            "toc": toc,
            "pages": len(pages),
        }
    )

    # Unpack models from list
    texify_model, layout_model, order_model, edit_model, detection_model, ocr_model = (
        model_lst
    )

    # Identify text lines on pages
    surya_detection(
        doc,
        pages,
        detection_model,
        batch_multiplier=batch_multiplier,
    )
    flush_cuda_memory()

    # OCR pages as needed
    pages, ocr_stats = run_ocr(
        doc, pages, langs, ocr_model, batch_multiplier=batch_multiplier
    )
    flush_cuda_memory()

    out_meta["ocr_stats"] = ocr_stats
    if len([b for p in pages for b in p.blocks]) == 0:
        print(f"Could not extract any text blocks for {fname}")
        return "", out_meta

    surya_layout(doc, pages, layout_model, batch_multiplier=batch_multiplier)
    flush_cuda_memory()

    # Find headers and footers
    bad_span_ids = filter_header_footer(pages)
    out_meta["block_stats"] = {"header_footer": len(bad_span_ids)}

    # Add block types in
    annotate_block_types(pages)

    # Dump debug data if flags are set
    dump_bbox_debug_data(doc, pages)

    # Find reading order for blocks
    # Sort blocks by reading order
    surya_order(doc, pages, order_model, batch_multiplier=batch_multiplier)
    sort_blocks_in_reading_order(pages)
    flush_cuda_memory()

    # Fix code blocks
    code_block_count = identify_code_blocks(pages)
    out_meta["block_stats"]["code"] = code_block_count
    indent_blocks(pages)

    # Fix table blocks
    table_count = format_tables(pages)
    out_meta["block_stats"]["table"] = table_count

    for page in pages:
        for block in page.blocks:
            block.filter_spans(bad_span_ids)
            block.filter_bad_span_types()

    filtered, eq_stats = replace_equations(
        doc, pages, texify_model, batch_multiplier=batch_multiplier
    )
    flush_cuda_memory()
    out_meta["block_stats"]["equations"] = eq_stats

    # Extract images and figures
    if settings.EXTRACT_IMAGES:
        extract_images(doc, pages)

    # Split out headers
    split_heading_blocks(pages)
    find_bold_italic(pages)

    # Copy to avoid changing original data
    merged_lines = merge_spans(filtered)
    text_blocks = merge_lines(merged_lines)
    text_blocks = filter_common_titles(text_blocks)
    full_text = get_full_text(text_blocks)

    # Handle empty blocks being joined
    full_text = cleanup_text(full_text)

    # Replace bullet characters with a -
    full_text = replace_bullets(full_text)

    # Postprocess text with editor model
    full_text, edit_stats = edit_full_text(
        full_text, edit_model, batch_multiplier=batch_multiplier
    )
    flush_cuda_memory()
    out_meta["postprocess_stats"] = {"edit": edit_stats}
    doc_images = images_to_dict(pages)

    doc.close()

    return full_text, doc_images, out_meta
