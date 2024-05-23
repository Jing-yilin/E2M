# logging
import logging
import base64
import os

from api.core.converters.base_converter import (
    BaseConverter,
)
from api.core.marker.convert import convert_single_pdf
from api.core.marker.models import load_all_models
from api.core.marker.settings import Settings

model_list = load_all_models()

logger = logging.getLogger(__name__)


def _parse_pdf_and_return_markdown(
    pdf_file: bytes,
    start_page: int = 0,
    end_page: int = None,
    extract_images: bool = False,
):
    full_text, images, out_meta = convert_single_pdf(
        pdf_file, model_list, start_page=start_page, end_page=end_page
    )
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
        start_page = kwargs.get("start_page", 0)
        end_page = kwargs.get("end_page", None)
        extract_images = kwargs.get("extract_images", False)

        if extract_images is False:
            Settings.EXTRACT_IMAGES = False
        else:
            Settings.EXTRACT_IMAGES = True

        full_text, images, out_meta = _parse_pdf_and_return_markdown(
            self.file,
            start_page=start_page,
            end_page=end_page,
            extract_images=extract_images,
        )
        return full_text
