import os
import requests
from pathlib import Path

from dotenv import load_dotenv

import python_utils


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
        "user_ids": vk_client_id,
        "v": 5.131
    }
    response = requests.post(vk_api_photo_wall_upload_server, headers=headers, params=params)
    response.raise_for_status()

    text = response.json()
    return text


if __name__ == "__main__":
    load_dotenv()
    download_path = os.getenv("DOWNLOAD_PATH")
    vk_client_id = os.getenv("CLIENT_ID")
    vk_access_token = os.getenv("APPLICATION_VK_TOKEN")
    Path(download_path).mkdir(parents=True, exist_ok=True)

    test1 = get_groups_vk(vk_client_id, vk_access_token)
    test_groups = test1['response']['items']

    comics_information = python_utils.download_comics()
    print(comics_information)

    # test_information = get_wall_vk_upload_server(vk_client_id, vk_access_token)
    # print(test_information)
    # test_info_response = test_information.get('response')
    # print()
    # print(test_info_response.get("album_id"), test_info_response.get("upload_url"), test_info_response.get("user_id"))
