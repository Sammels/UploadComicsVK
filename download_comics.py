import os
import requests
from pathlib import Path

from dotenv import load_dotenv
from python_utils import download_comics


def get_groups_vk(vk_client_id: str, vk_access_token: str) -> str:
    """Function POST request to VK API used GROUP.GET method """
    vk_api_group_get_method = "https://api.vk.com/method/groups.get"

    headers = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "user_ids": vk_client_id,
        "v": 5.131
    }
    response = requests.post(vk_api_group_get_method, headers=headers, params=params)
    response.raise_for_status()

    text = response.json()
    return text


def get_wall_vk_upload_server(vk_client_id: str, vk_access_token: str) -> str:
    """Function POST request to VK API used PHOTO.WALL.UPLOAD.SERVER method """
    vk_api_photo_wall_upload_server = "https://api.vk.com/method/photos.getWallUploadServer"
    headers = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "group_id": vk_client_id,
        "v": 5.131
    }
    response = requests.post(vk_api_photo_wall_upload_server, headers=headers, params=params)
    response.raise_for_status()

    text = response.json()
    return text


def upload_photo_to_vk(url_link: str, filename: str)-> str:
    """Function load photo to vk server and return dict photo info"""
    with open(f"Files/{filename}", 'rb') as file:
        url = url_link
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        photo_load_info = response.json()

        return photo_load_info


def photo_save_wall_vk(group_id, photo_info, vk_access_token):
    vk_api_load_photo = "https://api.vk.com/method/photos.saveWallPhoto"

    header = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "group_id": group_id,
        "server": photo_info.get("server"),
        "photo": photo_info.get("photo"),
        "hash": photo_info.get("hash"),
        "v": 5.131
    }

    response = requests.post(vk_api_load_photo, params=params, headers=header)
    response.raise_for_status()

    save_photo_wall_info = response.json()
    return save_photo_wall_info


def public_photo_to_group_vk():
    pass


if __name__ == "__main__":
    load_dotenv()
    download_path = os.getenv("DOWNLOAD_PATH")
    vk_client_id = os.getenv("CLIENT_ID")
    vk_access_token = os.getenv("APPLICATION_VK_TOKEN")
    Path(download_path).mkdir(parents=True, exist_ok=True)

    group_number = get_groups_vk(vk_client_id, vk_access_token)

    if 221144900 in group_number['response']['items']:
        group = 221144900

    comics_information = download_comics()

    test_information = get_wall_vk_upload_server(group, vk_access_token)
    test_info_response = test_information.get('response')
    url_for_upload = test_info_response.get("upload_url")

    photo_info = upload_photo_to_vk(url_for_upload,  comics_information['name'])

    load_photo_to_server_vk = photo_save_wall_vk(group, photo_info, vk_access_token)