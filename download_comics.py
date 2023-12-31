import os
from shutil import rmtree
from pathlib import Path
import logging
import requests

from dotenv import load_dotenv
from python_utils import download_comics

VK_API_GROUP_GET_METHOD = "https://api.vk.com/method/groups.get"
VK_API_PHOTO_WALL_UPLOAD_SERVER = "https://api.vk.com/method/photos.getWallUploadServer"
VK_API_LOAD_PHOTO = "https://api.vk.com/method/photos.saveWallPhoto"
VK_API_LOAD_WALL_PHOTO = "https://api.vk.com/method/wall.post"


def get_wall_vk_upload_server(group_id: str, vk_access_token: str) -> str:
    """Function POST request to VK API used PHOTO.WALL.UPLOAD.SERVER method."""
    headers = {"Authorization": f"Bearer {vk_access_token}"}
    params = {"group_id": group_id, "v": 5.131}

    response = requests.post(
        VK_API_PHOTO_WALL_UPLOAD_SERVER, headers=headers, params=params
    )
    response.raise_for_status()
    upload_url = response.json().get("response").get("upload_url")

    return upload_url


def upload_photo_to_vk(url_link: str, filename: str) -> dict:
    """Function load photo to vk server and return dict photo info."""
    file_dir = Path.cwd() / "Files" / filename
    with open(f"{file_dir}", "rb") as file:
        url = url_link
        files = {
            "photo": file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    photo_load_info = response.json()
    logging.info(msg=f"статус код upload_photo_to_vk:  {response.status_code}")

    return photo_load_info


def photo_save_wall_vk(
    group_id: str,
    photo_server_id: int,
    photo_full_information: str,
    photo_hash: str,
    vk_access_token: str,
):
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "group_id": group_id,
        "server": photo_server_id,
        "photo": photo_full_information,
        "hash": photo_hash,
        "v": 5.131,
    }

    response = requests.post(VK_API_LOAD_PHOTO, params=params, headers=header)
    response.raise_for_status()
    upload_photo_to_wall_server = response.json()
    logging.info(msg=f"статус код photo_save_wall_vk:  {response.status_code}")
    return upload_photo_to_wall_server


def post_photo_to_wall_vk(group_id, attachments, vk_access_token, message):
    """Posting Photo, message, in group vk."""
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "owner_id": f"-{group_id}",
        "from_group": 1,
        "attachments": attachments,
        "message": message,
        "v": 5.131,
    }
    vk_server_response = requests.get(
        VK_API_LOAD_WALL_PHOTO, headers=header, params=params
    )
    vk_server_response.raise_for_status()
    public_post_info = vk_server_response.json()
    logging.info(
        msg=f"статус код post_photo_to_wall_vk:  {vk_server_response.status_code}"
    )
    return public_post_info

class VkApiError(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f'VK API error: {self.error_code}: {self.error_message}')
def check_for_vk_api_errors(response):
    if 'error' in response:
        raise VkApiError(response['error']['error_code'], response['error']['error_msg'])


if __name__ == "__main__":
    load_dotenv()
    download_path = os.getenv("DOWNLOAD_PATH")
    vk_access_token = os.getenv("APPLICATION_VK_TOKEN")
    Path(download_path).mkdir(parents=True, exist_ok=True)

    group = os.getenv("VK_GROUP_ID")
    try:
        comics_name, comics_alt_name = download_comics()

        photo_to_server = get_wall_vk_upload_server(group, vk_access_token)

        photo_ = upload_photo_to_vk(photo_to_server, comics_name)
        photo_server_id = photo_.get("server")
        photo_full_information = photo_.get("photo")
        photo_hash = photo_.get("hash")

        photo_to_server_vk = photo_save_wall_vk(
            group, photo_server_id, photo_full_information, photo_hash, vk_access_token
        )
        vk_server_response = photo_to_server_vk.get("response")
        owner_id = vk_server_response[0].get("owner_id")
        media_id = vk_server_response[0].get("id")

        attachments = f"photo{owner_id}_{media_id}"
        post_photo_to_wall_vk(group, attachments, vk_access_token, comics_alt_name)

    except VkApiError as error:
        print(f"Ошибка VK API (код ошибки - {error.error_code}): {error.error_message}")

    finally:
        del_dir = Path.cwd() / "Files"
        rmtree(del_dir)
