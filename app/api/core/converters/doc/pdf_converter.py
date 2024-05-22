import base64
import os

from api.core.converters.base_converter import (
    BaseConverter,
)
from api.core.marker.convert import convert_single_pdf
from api.core.marker.models import load_all_models
from api.core.marker.settings import Settings

model_list = load_all_models()


def _parse_pdf_and_return_markdown(pdf_file: bytes, extract_images: bool):
    full_text, images, out_meta = convert_single_pdf(pdf_file, model_list)
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

    def convert(self, extract_images: bool = False, *args, **kwargs) -> str:

        # using VikParuchuri / marker
        if extract_images is False:
            Settings.EXTRACT_IMAGES = False
            print("Print EXTRACT_IMAGES set to False")
        else:
            Settings.EXTRACT_IMAGES = True
        full_text, images, out_meta = _parse_pdf_and_return_markdown(
            self.file, extract_images
        )
        return full_text
