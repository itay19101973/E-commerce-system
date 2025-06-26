import os


def validate_file_path(path: str) -> bool:
    """
       Validates whether the given path exists.

       :param path: The file path to validate.
       :return: True if the file exists, False otherwise.
    """
    if not os.path.exists(path):
        print(f"file not found: {path}")
        return False

    return True
