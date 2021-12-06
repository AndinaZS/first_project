import requests
from datetime import datetime
import json
from pprint import pprint

with open('tok.txt', 'r') as file:
    token_ya = file.readline().strip()
    token_vk = file.readline().strip()

class Vk_To_Yandex:
    vk_url = 'https://api.vk.com/method/'
    ya_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    def __init__(self, token_vk, token_ya, owner_id, version='5.131'):
        self.owner_id = owner_id
        self.params_vk = {
            'owner_id': owner_id,
            'access_token': token_vk,
            'v': version
            }
        self.headers_ya = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_ya}'}

    def get_albums(self):
        func_url = self.vk_url + 'photos.getAlbums/'
        response = requests.get(func_url, params=self.params_vk).json()
        if response.get('error', 0):
            print('Информация надоступна. Попробуййте загрузить фото из служебных альбомов "profile", "wall", "saved"')
        else:
            for elem in response['response']['items']:
                print(f'ID {elem["id"]} название {elem["title"]}')
        return

    def save_foto(self, album_id='profile', num=5):
        func_url = self.vk_url + 'photos.get/'
        func_params = {
        'album_id' : album_id,
        'extended' : '1',
        'count': num,
        }
        response = requests.get(func_url, params={**self.params_vk, **func_params}).json()
        if response.get('error', 0):
            print('Что-то пошло не так. Возможно, пользователь ограничил доступ к фото')
        else:
            self.__create_folder(album_id)
            self.__create_json(response['response']['items'], album_id)

    def __create_json(self, response, album_id):
        file_name = self.owner_id + album_id
        with open(f'{file_name}.json', 'w') as write_file:
            set_filenames = set()
            for elem in response:
                if str(elem['likes']['count'])in set_filenames:
                    date = datetime.utcfromtimestamp(elem['date']).strftime('%d-%m-%Y')
                    file_name = str(elem['likes']['user_likes']) + str(date)
                else:
                    file_name = str(elem['likes']['count'])
                self.__upload_foto(url=elem['sizes'][-1]['url'],file_name=file_name)
                json.dump({'file_name': f'{file_name}.jpg', 'size': elem['sizes'][-1]['type']}, write_file)
                set_filenames.add(file_name)

    def __create_folder(self, album_id):
        func_url = self.ya_url
        folder_name = self.owner_id + album_id
        headers = self.headers_ya
        params = {'path': folder_name}
        response = requests.put(func_url, headers=headers, params=params)

    def __upload_foto(self, url, file_name):
        upload_url = self.ya_url + 'upload'
        headers = self.headers_ya
        params = {"url": url, 'path':f'{self.owner_id}/{file_name}'}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code == 202:
            print(f'файл {file_name}.jpg загружен')
        else:
            print(f'ошибка при згрузке файла {file_name}.jpg')

if __name__ == '__main__':
    test = Vk_To_Yandex(token_vk, token_ya,'6827002')
    pprint(test.get_albums())
    # test.save_foto('147059587')



    # dct = get_url_foto('1565606', 10)
    # create_folder('1565606')
