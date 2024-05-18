from .docx_converter import DocxConverter
from .doc_converter import DocConverter
from .html_converter import HtmlConverter
from .htm_converter import HtmConverter
from .epub_converter import EpubConverter
from .pdf_converter import PdfConverter
from .rtf_converter import RtfConverter

support_types = [
    "docx",
    "doc",
    "html",
    "htm",
    "epub",
    "pdf",
    "rtf",
]

__all__ = [
    "DocxConverter",
    "DocConverter",
    "HtmlConverter",
    "HtmConverter",
    "EpubConverter",
    "PdfConverter",
    "RtfConverter",
]
