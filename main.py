import requests
from pprint import pprint
from datetime import datetime

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
    for elem in res:
        if dct.get(str(elem['likes']['count']), 0):
            date = datetime.utcfromtimestamp(elem['date']).strftime('%d-%m-%Y')
            dct[str(elem['likes']['count']) + str(date)] = elem['sizes'][-1]['url']
        else:
            dct[str(elem['likes']['count'])] = elem['sizes'][-1]['url']
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
    params = {"url": 'https://sun9-29.userapi.com/c5130/u1565606/-6/m_40291f0b.jpg', 'path':'Новая папка/1'}
    response = requests.post(upload_url, headers=headers, params=params)
    pprint(response.status_code)

if __name__ == '__main__':
    pprint(get_url_foto('1565606', 10))
