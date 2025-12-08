import requests


def get_file_extension(filename: str) -> str:
    return "." + filename.lower().split(".")[-1] if "." in filename else ""


def fetch_url_content(url: str) -> requests.Response:
    return requests.get(
        url, headers={"User-Agent": "ExtractLab/0.1 (https://github.com/HrunytskyiDS; ipzm242_gds@student.ztu.edu.ua)"}
    )
