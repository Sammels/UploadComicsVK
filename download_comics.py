import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from python_utils import download_comics, remove_file_afret_download


VK_API_GROUP_GET_METHOD = "https://api.vk.com/method/groups.get"
VK_API_PHOTO_WALL_UPLOAD_SERVER = "https://api.vk.com/method/photos.getWallUploadServer"
VK_API_LOAD_PHOTO = "https://api.vk.com/method/photos.saveWallPhoto"
VK_API_LOAD_WALL_PHOTO = "https://api.vk.com/method/wall.post"

def get_groups_vk(vk_client_id: str, vk_access_token: str) -> str:
    """Function POST request to VK API used GROUP.GET method """

    headers = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "user_ids": vk_client_id,
        "v": 5.131
    }
    response = requests.post(VK_API_GROUP_GET_METHOD, headers=headers, params=params)
    response.raise_for_status()
    text = response.json()
    return text


def get_wall_vk_upload_server(group_id: str, vk_access_token: str) -> str:
    """Function POST request to VK API used PHOTO.WALL.UPLOAD.SERVER method """
    headers = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "group_id": group_id,
        "v": 5.131
    }
    response = requests.post(VK_API_PHOTO_WALL_UPLOAD_SERVER, headers=headers, params=params)
    response.raise_for_status()
    text = response.json()
    return text


def upload_photo_to_vk(url_link: str, filename: str) -> str:
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

    response = requests.post(VK_API_LOAD_PHOTO, params=params, headers=header)
    response.raise_for_status()
    save_photo_wall_info = response.json()
    return save_photo_wall_info


def public_photo_to_group_vk(group_id, attachments, vk_access_token, message):

    header = {
        "Authorization": f"Bearer {vk_access_token}"
    }
    params = {
        "owner_id": f"-{group_id}",
        "from_group": 1,
        "attachments": attachments,
        "message": message,
        "v": 5.131
    }
    vk_server_response = requests.get(VK_API_LOAD_WALL_PHOTO, headers=header, params=params)
    vk_server_response.raise_for_status()
    awesome_style = vk_server_response.json()
    return awesome_style


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

    upload_photo_to_server = get_wall_vk_upload_server(group, vk_access_token)
    test_info_response = upload_photo_to_server.get('response')
    url_for_upload = test_info_response.get("upload_url")

    photo_info = upload_photo_to_vk(url_for_upload,  comics_information['name'])
    load_photo_to_server_vk = photo_save_wall_vk(group, photo_info, vk_access_token)
    vk_server_response = load_photo_to_server_vk.get('response')
    owner_id = vk_server_response[0].get("owner_id")
    media_id = vk_server_response[0].get("id")

    attachments = f"photo{owner_id}_{media_id}"
    public_photo_to_group_vk(group, attachments, vk_access_token, comics_information['alternative_name'])
    remove_file_afret_download()