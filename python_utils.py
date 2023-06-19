import os
import requests

from random import randint
from urllib.parse import urlsplit


def get_file_extension(url: str) -> str:
    """Function get http link and return file extension"""
    url = urlsplit(url)[2]
    template = os.path.splitext(url)
    _, *extension = template
    return extension[0]


def download_comics() -> dict[str, str]:
    """Function download comics and return name, alternative name"""
    random_comics_number = randint(1, 2788)
    test_url = f"https://xkcd.com/{random_comics_number}/info.0.json"

    response = requests.get(test_url)
    response.raise_for_status()
    comics = response.json()
    comics_image_link = comics.get('img')
    alt_comics_name = comics.get('alt')
    print(alt_comics_name)

    # extension
    extension = get_file_extension(comics_image_link)

    # Download image
    download_comics = requests.get(comics_image_link)
    download_comics.raise_for_status()
    with open(f'Files/comics_{random_comics_number}{extension}', 'wb') as file:
        file.write(download_comics.content)

    comics_name = f"comics_{random_comics_number}{extension}"

    return {"name": comics_name, "alternative_name": alt_comics_name}