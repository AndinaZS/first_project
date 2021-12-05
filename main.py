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
    res = requests.get(url, params=params).json()['response']['items']
    with open("data_file.json", "w") as write_file:
        for elem in res:
            if dct.get(str(elem['likes']['count']), 0):
                date = datetime.utcfromtimestamp(elem['date']).strftime('%d-%m-%Y')
                file_name = str(elem['likes']['user_likes']) + str(date)
            else:
                file_name = str(elem['likes']['count'])
            dct[file_name] = elem['sizes'][-1]['url']
            json.dump({'file_name': f'{file_name}.jpg', 'size': elem['sizes'][-1]['type']}, write_file)
    return dct

def create_folder(folder_name):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_ya}'}
    params = {'path': folder_name}
    response = requests.put(upload_url, headers=headers, params=params)

def upload_foto(dct_foto):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json',
            'Authorization': f'OAuth {token_ya}'}
    for key, value in dct_foto.items():
        params = {"url": value, 'path':f'1565606/{key}'}
        response = requests.post(upload_url, headers=headers, params=params)
        pprint(response.status_code)

if __name__ == '__main__':
    dct = get_url_foto('1565606', 10)
    create_folder('1565606')
    upload_foto(dct)
