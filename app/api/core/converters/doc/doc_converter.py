import logging
import os
import subprocess

from pathlib import Path
from api.core.converters.base_converter import (
    BaseConverter,
)

from api.blueprints.v1.schemas import ResponseData, FileInfo, RequestData


logger = logging.getLogger(__name__)


def _convert_doc_to_docx(doc_path: str, docx_path: str):
    # Construct the command to convert .doc to .docx using LibreOffice
    # you have to install LibreOffice on your system
    # Ubuntu: sudo apt-get install libreoffice
    # MacOS: brew install --cask libreoffice
    # Windows: download from https://www.libreoffice.org/
    command = [
        "soffice",
        "--headless",
        "--convert-to",
        "docx",
        doc_path,
        "--outdir",
        os.path.dirname(docx_path),
    ]

    # Execute the command
    subprocess.run(command, check=True)

    # Rename the converted file to the desired .docx filename if necessary
    converted_file = os.path.join(
        os.path.dirname(doc_path),
        os.path.splitext(os.path.basename(doc_path))[0] + ".docx",
    )
    if converted_file != docx_path:
        os.rename(converted_file, docx_path)


class DocConverter(BaseConverter):

    def convert(
        self,
        file_info: FileInfo,
        request_data: RequestData,
        **kwargs,
    ) -> ResponseData:
        # save as docx
        if isinstance(self.file, str) and self.file.endswith(".doc"):
            stem = os.path.splitext(self.file)[0]
        elif isinstance(self.file, Path) and self.file.suffix == ".doc":
            stem = self.file.stem
        else:
            raise ValueError("Unsupported file type")
        out_file = f"{stem}.docx"

        content = ""

        try:
            logger.info(f"Converting [{self.file}] to [{out_file}]")
            _convert_doc_to_docx(self.file, out_file)
            logger.info(f"Converted [{self.file}] to [{out_file}]")

            from api.core.converters.doc.docx_converter import DocxConverter

            docx_converter = DocxConverter(file=out_file, parse_mode=self.parse_mode)
            content = docx_converter.convert(
                file_info=file_info, request_data=request_data, **kwargs
            )
        except Exception as e:
            logger.error(f"Error converting file: {self.file}, error: {e}")
        finally:
            self.rm_file()

        return content
