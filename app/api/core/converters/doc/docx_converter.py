from api.core.converters.base_converter import (
    BaseConverter,
)

from api.core.converters.md_elements import (
    Header1,
    Header2,
    Header3,
    Paragraph,
    MdElement,
    MarkdownPage,
)
from api.blueprints.v1.schemas import ResponseData, FileInfo, RequestData


import json
from typing import List

from api.config import Config

# logging
import logging

logger = logging.getLogger(__name__)


class DocxConverter(BaseConverter):

    def convert(
        self,
        file_info: FileInfo,
        request_data: RequestData,
        **kwargs,
    ) -> ResponseData:

        elements: List[MdElement] = []

        # method 1： default
        if Config.DOCX_CONVERTER == "default":
            logger.info(f"Converting [{self.file}] with default converter")
            from docx import Document

            doc = Document(self.file)

            """
            {
                "font size": {
                    "type": "header1",
                    "freq: 0.31,
                    "count": 100,
                    "paragraph": [1, 2, 3]
                },
                ...
            }

            """

            font_size_count = {}
            total_runs = 0

            for i, paragraph in enumerate(doc.paragraphs):
                if not paragraph.text.strip():
                    continue
                for run in paragraph.runs:
                    font_size = run.font.size
                    if not font_size:
                        continue
                    total_runs += 1
                    if font_size not in font_size_count:
                        font_size_count[font_size] = {"count": 1, "paragraph": [i]}
                    else:
                        font_size_count[font_size]["count"] += 1
                        font_size_count[font_size]["paragraph"].append(i)

            if not font_size_count:
                return ""

            all_font_size = set(font_size_count.keys())
            logger.debug(f"all_font_size: {all_font_size}")
            all_font_size = sorted(all_font_size, reverse=True)

            header1_font_size = 0
            header2_font_size = 0
            header3_font_size = 0

            # calculate the frequency of each font size
            for font_size in font_size_count:
                font_size_count[font_size]["freq"] = (
                    font_size_count[font_size]["count"] / total_runs
                )
                # if the frequency of a font size is greater than 0.8, it is a paragraph
                if font_size_count[font_size]["freq"] > 0.8:
                    font_size_count[font_size]["type"] = "paragraph"
                else:
                    # if the frequency of a font size is less than 0.8, it is a header
                    if len(all_font_size) >= 2 and font_size == all_font_size[0]:
                        font_size_count[font_size]["type"] = "header1"
                        header1_font_size = font_size
                    elif len(all_font_size) >= 3 and font_size == all_font_size[1]:
                        font_size_count[font_size]["type"] = "header2"
                        header2_font_size = font_size
                    elif len(all_font_size) >= 4 and font_size == all_font_size[2]:
                        font_size_count[font_size]["type"] = "header3"
                        header3_font_size = font_size

            logger.info(f"font_size_count: {font_size_count}")

            for para in doc.paragraphs:
                if not para.text.strip():
                    continue

                if para.runs[0].font.size == header1_font_size:
                    elements.append(Header1(text=para.text))
                elif para.runs[0].font.size == header2_font_size:
                    elements.append(Header2(text=para.text))
                elif para.runs[0].font.size == header3_font_size:
                    elements.append(Header3(text=para.text))
                else:
                    elements.append(Paragraph(text=para.text))

        # method 2: unstructured
        elif Config.DOCX_CONVERTER == "unstructured":
            logger.info(f"Converting [{self.file}] with unstructured converter")
            from unstructured.partition.docx import partition_docx

            unstructured_elements = partition_docx(filename=self.file)
            for element in unstructured_elements:
                # todo: need a more accurate way to determine the category
                # if element.category == "Title":
                #     elements.append(Header1(element.text))
                # else:
                elements.append(Paragraph(text=element.text))

        else:
            raise ValueError(
                f"Invalid CONVERTER: {Config.DOCX_CONVERTER}, you should set\
                      CONVERTER to 'default' or 'unstructured'"
            )

        self.rm_file()
        result = MarkdownPage.from_elements(elements)

        use_llm = request_data.use_llm

        if Config.ENABLE_LLM and use_llm:

            model = request_data.model
            return_type = request_data.return_type
            enforced_json_format = request_data.enforced_json_format

            if return_type == "json":
                fixed_result = self.ocr_fix_to_json(
                    result, enforced_json_format=enforced_json_format, model=model
                )
                fixed_result = json.dumps(fixed_result, ensure_ascii=False, indent=4)
            elif return_type == "md":
                fixed_result = self.ocr_fix_to_markdown(result, model=model)
                return MarkdownPage.from_md(fixed_result)
            else:
                raise ValueError("return_type must be one of 'md' or 'json")

            return fixed_result

        return result
