from ..base_converter import (
    BaseConverter,
    MdElement,
    Header1,
    Header2,
    Header3,
    Paragraph,
    merge_elements_to_md,
)

from typing import List

from ....config import Config

# logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class DocxConverter(BaseConverter):

    def convert(self) -> str:
        if not self.file:
            raise ValueError("File not set")
        # todo: a better to convert docx to markdown
        elements: List[MdElement] = []

        if Config.CONVERTER == "default":
            logger.info(f"Converting [{self.file}] with default converter")
            from docx import Document

            doc = Document(self.file)
            # 获取header和paragraph
            for para in doc.paragraphs:
                if para.style.name == "Heading 1":
                    elements.append(Header1(para.text))
                elif para.style.name == "Heading 2":
                    elements.append(Header2(para.text))
                elif para.style.name == "Heading 3":
                    elements.append(Header3(para.text))
                else:
                    elements.append(Paragraph(para.text))
        elif Config.CONVERTER == "unstructured":
            logger.info(f"Converting [{self.file}] with unstructured converter")
            from unstructured.partition.docx import partition_docx

            unstructured_elements = partition_docx(filename=self.file)
            for element in unstructured_elements:
                # todo: need a more accurate way to determine the category
                if element.category == "Title":
                    elements.append(Header1(element.text))
                else:
                    elements.append(Paragraph(element.text))

        else:
            raise ValueError(
                f"Invalid CONVERTER: {Config.CONVERTER}, you should set\
                      CONVERTER to 'default' or 'unstructured'"
            )

        return merge_elements_to_md(elements)
