def get_file_extension(filename: str) -> str:
    return "." + filename.lower().split(".")[-1] if "." in filename else ""
