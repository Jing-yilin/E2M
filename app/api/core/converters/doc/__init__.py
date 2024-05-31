from api.core.converters.doc.txt_converter import TxtConverter
from api.core.converters.doc.docx_converter import DocxConverter
from api.core.converters.doc.doc_converter import DocConverter
from api.core.converters.doc.html_converter import HtmlConverter
from api.core.converters.doc.htm_converter import HtmConverter
from api.core.converters.doc.epub_converter import EpubConverter
from api.core.converters.doc.pdf_converter import PdfConverter
from api.core.converters.doc.rtf_converter import RtfConverter


support_types = [
    "md",
    "py",
    "json",
    "yaml",
    "yml",
    "txt",
    "docx",
    "doc",
    "html",
    "htm",
    "epub",
    "pdf",
    "rtf",
]

__all__ = [
    "TxtConverter",
    "DocxConverter",
    "DocConverter",
    "HtmlConverter",
    "HtmConverter",
    "EpubConverter",
    "PdfConverter",
    "RtfConverter",
]
