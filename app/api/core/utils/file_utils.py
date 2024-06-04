from typing import Union, Literal
import os
import subprocess
import logging

logger = logging.getLogger(__name__)


def convert_doc_to_docx(doc_path: str, docx_path: str, rm_original: bool = True):
    """Convert a .doc file to a .docx file.

    Args:
        doc_path: The path to the .doc file.
        docx_path: The path to the .docx file.
        rm_original: Whether to remove the original .doc file after conversion.

    Raises:
        subprocess.CalledProcessError: If the conversion command fails.

    """
    logger.info(f"Converting [{doc_path}] to [{docx_path}]")
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

    # Remove the original .doc file
    if rm_original:
        os.remove(doc_path)


def get_file_hash(
    file: Union[str, bytes],
    hash_type: Literal["md5", "sha256"] = "md5",
    chunk_size: int = 4096,
) -> str:
    """
    Calculate the hash of a file.

    Args:
        file: The file to hash.

    Returns:
        The hash of the file.
    """
    import hashlib

    # choose hash type
    if hash_type == "md5":
        hasher = hashlib.md5()
    elif hash_type == "sha256":
        hasher = hashlib.sha256
    else:
        raise ValueError(f"Invalid hash type: {hash_type}")

    # calculate hash for file
    if isinstance(file, str):
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
            # reset file pointer
            f.seek(0)
    elif isinstance(file, bytes):
        hasher.update(file)
    else:
        raise ValueError("Invalid file type")

    return hasher.hexdigest()
