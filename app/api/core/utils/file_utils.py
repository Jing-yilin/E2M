from typing import Union, Literal


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
