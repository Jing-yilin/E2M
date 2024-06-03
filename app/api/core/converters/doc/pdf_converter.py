import logging
from tqdm import tqdm
import base64
import os
from api.core.converters.base_converter import (
    BaseConverter,
)
from api.core.marker.settings import Settings
from api.config import Config

from api.core.converters.md_elements import (
    Paragraph,
    merge_elements_to_md,
)

from api.blueprints.v1.schemas import ResponseData, FileInfo, RequestData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _parse_pdf_and_return_markdown(
    pdf_file: bytes,
    extract_images: bool = False,
    langs: list = ["zh"],
):
    from api.core.marker.convert import convert_single_pdf
    from api.core.marker.models import ModelHandler

    model_list = ModelHandler.get_models(langs=langs)

    if not os.path.exists(Config.TRANSFORMERS_CACHE):
        os.makedirs(Config.TRANSFORMERS_CACHE)

    full_text, images, out_meta = convert_single_pdf(pdf_file, model_list, langs=langs)
    # todo: to handle images
    image_data = {}
    if extract_images:
        for i, (filename, image) in enumerate(images.items()):
            # Save image as PNG
            if not os.path.exists("temp"):
                os.makedirs("temp")
            image_filepath = f"temp/image_{i+1}.png"
            image.save(image_filepath, "PNG")

            # Read the saved image file as bytes
            with open(image_filepath, "rb") as f:
                image_bytes = f.read()

            # Convert image to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            image_data[f"image_{i+1}"] = image_base64

            # Remove the temporary image file
            os.remove(image_filepath)

    return full_text, out_meta, image_data


class PdfConverter(BaseConverter):

    def convert(
        self,
        file_info: FileInfo,
        request_data: RequestData,
        **kwargs,
    ) -> ResponseData:

        logger.info(f"Converting PDF file to markdown: {self.file}")
        logger.info(f"kwargs: {kwargs}")

        extract_images = request_data.extract_images
        parse_mode = request_data.parse_mode
        # you can find supported languages in https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016
        langs = request_data.langs
        first_page = request_data.first_page
        last_page = request_data.last_page
        use_llm = request_data.use_llm
        model = request_data.model
        return_type = request_data.return_type
        enforced_json_format = request_data.enforced_json_format

        if Config.PDF_CONVERTER == "default" or parse_mode == "ocr_high":

            # save pdf as images into a pdf
            # images = convert_from_path(test_pdf, first_page=page_number, last_page=page_number)
            temp_dir = "temp/image_pdf"
            new_pdf_name = self.file_stem + "_images.pdf"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            from pdf2image import convert_from_path

            images = convert_from_path(
                self.file, first_page=first_page, last_page=last_page
            )
            all_single_image_pdfs = []
            # save images to a pdf
            for i, image in enumerate(images):
                all_single_image_pdfs.append(
                    f"{temp_dir}/{new_pdf_name}_{i+first_page}.pdf"
                )
                image.save(f"{temp_dir}/{new_pdf_name}_{i+first_page}.pdf")

            if extract_images is False:
                Settings.EXTRACT_IMAGES = False
            else:
                Settings.EXTRACT_IMAGES = True

            content = []
            for idx, single_image_pdf in tqdm(
                enumerate(all_single_image_pdfs), total=len(all_single_image_pdfs)
            ):
                logger.info(
                    f"[{idx+1}/{len(all_single_image_pdfs)}] Processing {single_image_pdf}..."
                )
                full_text, out_meta, image_data = _parse_pdf_and_return_markdown(
                    single_image_pdf,
                    extract_images=extract_images,
                    langs=langs,
                )
                logger.info(
                    f"[{idx+1}/{len(all_single_image_pdfs)}]full_text: {full_text}"
                )
                content.append(full_text)
                # rm single image pdf
                if os.path.exists(single_image_pdf):
                    os.remove(single_image_pdf)

            raw_result = "\n".join(content)

        elif Config.PDF_CONVERTER == "unstructured":
            logger.info(f"Converting [{self.file}] with unstructured converter")
            from unstructured.partition.pdf import partition_pdf

            # from unstructured.partition.lang import PYTESSERACT_LANG_CODES
            import fitz

            # todo: support multiple languages
            lang_map = {
                "zh": "chi_sim",
                "en": "eng",
            }
            new_langs = []
            for lang in langs:
                new_langs.append(lang_map[lang])

            # from first_page to last_page
            fitz_pdf = fitz.open(self.file)
            total_pages = fitz_pdf.page_count
            # rm other pages, only keep the first page -> last page
            logger.info(f"fitz_pdf.page_count: {fitz_pdf.page_count}")
            # delete right
            if last_page is not None:
                from_page = last_page
                fitz_pdf.delete_pages(from_page=from_page, to_page=total_pages - 1)
            logger.info(f"fitz_pdf.page_count: {fitz_pdf.page_count}")

            if first_page > 1:
                to_page = first_page - 1
                fitz_pdf.delete_pages(from_page=0, to_page=to_page - 1)

            logger.info(f"fitz_pdf.page_count: {fitz_pdf.page_count}")

            # save to original pdf
            tmp_file = self.file + ".tmp"
            fitz_pdf.save(self.file + ".tmp")

            if parse_mode == "auto":
                strategy = "auto"
            elif parse_mode == "ocr_low":
                strategy = "ocr_only"
            elif parse_mode == "fast":
                strategy = "fast"
            else:
                strategy = "auto"

            # "hi_res", "ocr_only", and "fast".
            unstructured_elements = partition_pdf(
                filename=tmp_file,
                languages=new_langs,
                extract_images_in_pdf=extract_images,
                starting_page_number=first_page,
                # extract_forms=True,
                # form_extraction_skip_tables=False,
                strategy=strategy,
            )
            elements = []
            for element in unstructured_elements:
                logger.debug(f"element: {element.metadata.to_dict()}")
                # if element.category == "Title":
                #     elements.append(Header1(element.text))
                # else:
                elements.append(Paragraph(text=element.text))

            raw_result = merge_elements_to_md(elements)

            # rm tmp
            os.remove(tmp_file)

        else:
            raise ValueError(f"Unknown PDF_CONVERTER: {Config.PDF_CONVERTER}")

        self.rm_file()

        if not (Config.ENABLE_LLM and use_llm):
            self.set_response_data(status="success", raw=raw_result)
        else:
            try:
                if return_type == "json":
                    self.ocr_fix_to_json(
                        raw_result,
                        enforced_json_format=enforced_json_format,
                        model=model,
                    )
                elif return_type == "md":
                    self.ocr_fix_to_markdown(raw_result, model=model)
                else:
                    raise ValueError("return_type must be one of 'md' or 'json'")
                self.set_response_data(status="success", raw=raw_result)
            except Exception as e:
                logger.error(f"Error in LLM: {e}")
                self.set_response_data(status="error", raw=raw_result, error=str(e))

        return self.resp_data
