import logging
from tqdm import tqdm
import base64
import os
from api.core.converters.base_converter import (
    BaseConverter,
)
from api.core.marker.settings import Settings
from api.config import Config

logger = logging.getLogger(__name__)


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
        **kwargs,
    ) -> str:

        logger.info(f"Converting PDF file to markdown: {self.file}")
        logger.info(f"kwargs: {kwargs}")

        # using VikParuchuri / marker
        extract_images = kwargs.get("extract_images", False)
        # you can find supported languages in https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016
        langs = kwargs.get("langs", ["zh"])
        first_page = kwargs.get("first_page", 1)
        last_page = kwargs.get("last_page", None)

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
            logger.info(f"[{idx+1}/{len(all_single_image_pdfs)}]full_text: {full_text}")
            content.append(full_text)
            # rm single image pdf
            if os.path.exists(single_image_pdf):
                os.remove(single_image_pdf)

        self.rm_file()

        return "\n".join(content)
