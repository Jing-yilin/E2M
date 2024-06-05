from api.core.converters.doc.docx_converter import DocxConverter
from api.core.converters.doc.html_converter import HtmlConverter
from api.core.converters.doc.epub_converter import EpubConverter
from api.core.converters.doc.pdf_converter import PdfConverter
from api.core.converters.doc.pptx_converter import PptxConverter
from api.core.converters.doc.rtf_converter import RtfConverter


ALL_SUPPORT_TYPES = [
    "docx",
    "doc",
    "html",
    "htm",
    "epub",
    "pdf",
    "pptx",
    "rtf",
]

__all__ = [
    "DocxConverter",
    "HtmlConverter",
    "EpubConverter",
    "PdfConverter",
    "PptxConverter",
    "RtfConverter",
]
