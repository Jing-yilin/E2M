from api.core.converters.base_converter import BaseConverter
from api.core.marker.settings import Settings
from api.blueprints.v1.schemas import ResponseData
from api.config import Config

from tqdm import tqdm
import base64
import os

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _parse_pdf_and_return_markdown(
    pdf_file: bytes,
    extract_images: bool = False,
    langs: list = ["zh"],
):
    """OCR-High Parse Mode"""
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

    @classmethod
    def allowed_formats(cls) -> list[str]:
        return ["pdf"]

    def convert(
        self,
        **kwargs,
    ) -> ResponseData:

        logger.info(f"Converting PDF file to markdown: {self.file}")
        logger.info(f"kwargs: {kwargs}")

        extract_images = self.request_data.extract_images
        parse_mode = self.request_data.parse_mode
        # you can find supported languages in https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016
        langs = self.request_data.langs
        first_page = self.request_data.first_page
        last_page = self.request_data.last_page
        use_llm = self.request_data.use_llm

        tmp_file = self.file + ".tmp"
        from api.core.utils.file_utils import sub_pdf

        sub_pdf(self.file, first_page, last_page, tmp_file)

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

            raw = "\n".join(content)

        elif Config.PDF_CONVERTER == "unstructured":
            logger.info(f"Converting [{self.file}] with unstructured converter")
            from unstructured.partition.pdf import partition_pdf

            # from unstructured.partition.lang import PYTESSERACT_LANG_CODES
            # todo: support multiple languages
            lang_map = {
                "zh": "chi_sim",
                "en": "eng",
            }
            new_langs = []
            for lang in langs:
                if lang not in lang_map:
                    raise ValueError(f"Unsupported language: {lang}")
                new_langs.append(lang_map[lang])

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

            raw = "\n\n".join([element.text for element in unstructured_elements])

        else:
            raise ValueError(f"Invalid PDF_CONVERTER: {Config.PDF_CONVERTER}")

        if Config.ENABLE_LLM and use_llm:
            self.llm_enforce(raw)

        self.set_response_data(status="success", raw=raw)
        os.remove(tmp_file)
        return self.resp_data
