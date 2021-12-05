import requests
from pprint import pprint
from datetime import datetime
import json

with open('tok.txt', 'r') as file:
    token_ya = file.readline().strip()
    token_vk = file.readline().strip()
def get_url_foto(ownerID, num=5):
    dct = {}
    url = 'https://api.vk.com/method/photos.get/'
    params = {
    'owner_id' : ownerID,
    'album_id' : 'profile',
    'extended' : '1',
    'count': num,
    'access_token': token_vk,
    'v':'5.131'}
    response = requests.get(url, params=params).json()['response']['items']
    create_json(response)
    return

def create_json(response):
    with open("data_file.json", "w") as write_file:
        set_filenames = set()
        for elem in response:
            if str(elem['likes']['count'])in set_filenames:
                date = datetime.utcfromtimestamp(elem['date']).strftime('%d-%m-%Y')
                file_name = str(elem['likes']['user_likes']) + str(date)
            else:
                file_name = str(elem['likes']['count'])
            upload_foto(url=elem['sizes'][-1]['url'],file_name=file_name)
            json.dump({'file_name': f'{file_name}.jpg', 'size': elem['sizes'][-1]['type']}, write_file)
            set_filenames.add(file_name)
    return

def create_folder(folder_name):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_ya}'}
    params = {'path': folder_name}
    response = requests.put(upload_url, headers=headers, params=params)

def upload_foto(url, file_name):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json',
            'Authorization': f'OAuth {token_ya}'}
    params = {"url": url, 'path':f'1565606/{file_name}'}
    response = requests.post(upload_url, headers=headers, params=params)
    pprint(response.status_code)

if __name__ == '__main__':
    dct = get_url_foto('1565606', 10)
    create_folder('1565606')
