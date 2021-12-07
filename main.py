import requests
from datetime import datetime
import json

with open('tokens.txt', 'r') as file:
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
        self.headers_ya = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token_ya}'
            }

    def get_albums(self):
        func_url = self.vk_url + 'photos.getAlbums/'
        response = requests.get(func_url, params=self.params_vk).json()
        if response.get('error', 0):
            print('Информация надоступна. Попробуйте загрузить фото '
                  'из служебных альбомов "profile", "wall", "saved"')
        else:
            for elem in response['response']['items']:
              print(f'ID {elem["id"]} название {elem["title"]}')
        return

    def save_foto(self, album_id='profile'):
        num = input('Какое количество фото вы хотите загрузить (от 1 до 1000): ')
        if not num.isdigit() or  1000 < int(num) <1:
            num = 5
            print('Вы ввели неверное значение. Будут загружены 5 фото')
        else:
            num = int(num)
        self.path = self.owner_id + album_id
        func_url = self.vk_url + 'photos.get/'
        func_params = {
        'album_id' : album_id,
        'extended' : '1',
        'count': num,
        }
        response = requests.get(func_url, params={**self.params_vk, **func_params}).json()
        if response.get('error', 0):
            print('Что-то пошло не так. Возможно, пользователь ограничил доступ '
                  'к фото альбома или альбома не существует.')
        else:
            self.__create_folder()
            self.__create_json(response['response']['items'])
        return

    def __create_folder(self):
        func_url = self.ya_url
        headers = self.headers_ya
        params = {'path': self.path}
        response = requests.put(func_url, headers=headers, params=params)
        return

    def __create_json(self, response):
        data_json = []
        set_filenames = set()
        for elem in response:
            if str(elem['likes']['count']) in set_filenames:
                date = datetime.utcfromtimestamp(elem['date']).strftime('%d-%m-%Y')
                file_name = str(elem['likes']['user_likes']) + str(date)
            else:
                file_name = str(elem['likes']['count'])
            self.__upload_foto(url=elem['sizes'][-1]['url'],file_name=file_name)
            data_json.append({'file_name': f'{file_name}.jpg', 'size': elem['sizes'][-1]['type']})
            set_filenames.add(file_name)
        with open(f'{self.path}.json', 'w') as write_file:
            json.dump(data_json, write_file, indent=2)
        return

    def __upload_foto(self, url, file_name):
        upload_url = self.ya_url + 'upload'
        headers = self.headers_ya
        params = {"url": url, 'path':f'{self.path}/{file_name}'}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code == 202:
            print(f'файл {file_name}.jpg загружен')
        else:
            print(f'ошибка при згрузке файла {file_name}.jpg')
        return

if __name__ == '__main__':
    test = Vk_To_Yandex(token_vk, token_ya,'1565606')
    test.get_albums()
    test.save_foto('wall')


