import os


def validate_file_path(path):
    if not os.path.exists(path):
        print(f"file not found: {path}")
        return False

    return True
