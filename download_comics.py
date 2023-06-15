import os
import requests




def download_image():
    """Function download image"""
    pass

if __name__ == "__main__":
    '''1. Сделать запрос
    2. достать номер комикса
    3. Вставить номер , и скачать по жсону
    
    или
    спарсить мета,
    скачать.
    '''
    comics_url = "https://c.xkcd.com/random/comic/"
    test_url = "https://xkcd.com/2163/info.0.json"

    response = requests.get(comics_url)
    response.raise_for_status()

    #comics = response.json()
    comics = response.text

    print(comics)