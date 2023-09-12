import os
from typing import Any, Tuple

import requests

from random import randint
from urllib.parse import urlsplit
from pathlib import Path


def get_file_extension(url: str) -> str:
    """Function get http link and return file extension"""
    url = urlsplit(url)[2]
    template = os.path.splitext(url)
    _, *extension = template
    return extension[0]


def download_comics() -> tuple[str, Any]:
    """Function download comics and return name, alternative name"""
    comics_min_number = 1
    comics_max_number = 2788
    random_comics_number = randint(comics_min_number, comics_max_number)
    test_url = f"https://xkcd.com/{random_comics_number}/info.0.json"

    response = requests.get(test_url)
    response.raise_for_status()
    comics = response.json()
    comics_image_link = comics.get("img")
    alt_comics_name = comics.get("alt")

    extension = get_file_extension(comics_image_link)

    download_comics = requests.get(comics_image_link)
    download_comics.raise_for_status()
    file_dir = Path.cwd() / "Files" / f"comics_{random_comics_number}{extension}"
    with open(file_dir, "wb") as file:
        file.write(download_comics.content)

    comics_name = f"comics_{random_comics_number}{extension}"

    return comics_name, alt_comics_name
