import os
import requests
from random import randint
from pathlib import Path

from dotenv import load_dotenv
from urllib.parse import urlsplit



def get_file_extension(url: str) -> str:
    """Function get http link and return file extension"""
    url = urlsplit(url)[2]
    template = os.path.splitext(url)
    file_link, *extension = template
    return extension[0]


def download_image():
    """Function download image"""
    random_comics_number = randint(1, 2788)
    comics_url = "https://c.xkcd.com/random/comic/"
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
    with open(f'Files/comics{random_comics_number}{extension}', 'wb') as file:
        file.write(download_comics.content)


def test_vk_post(vk_client_id, vk_access_token):
    vk_api = "https://api.vk.com/method/"
    group_get_method = vk_api + "groups.get"

    headers = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "user_ids": vk_client_id,
        "v": 5.131
    }
    response = requests.post(group_get_method, headers=headers, params=params)
    response.raise_for_status()

    text = response.json()
    return text



if __name__ == "__main__":
    load_dotenv()
    download_path = os.getenv("DOWNLOAD_PATH")
    vk_client_id = os.getenv("CLIENT_ID")
    vk_access_token = os.getenv("APPLICATION_VK_TOKEN")
    Path(download_path).mkdir(parents=True, exist_ok=True)

    test1 = test_vk_post(vk_client_id, vk_access_token)
    print(test1)




