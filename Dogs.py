import requests
import os
import json
from settings import token

def create_internal_folder_yadisk(token, breed):
    headers = {
        'Authorization' : f'OAuth {token}'
    }
    params = {
        'path' : f'dogs/{breed}'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers = headers, params = params)
    if response.ok:
        print(f'Папка {breed} создана')
    else:
        print(f'Папка {breed} не создана')

def load_picture_yadisk(picture_url, file_name, token, breed):
    headers = {
        'Authorization' : f'OAuth {token}'
    }
    params = {
        'url' : picture_url,
        'path' : f'dogs/{breed}/{file_name}'
    }
    response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers = headers, params = params)
    if response.ok:
        print(f'Файл {file_name} загружен')
    else:
        print(f'Файл {file_name} не загружен')

def write_to_json(new_list):
    file_path = 'data.json'
    if os.path.exists(file_path):
        with open('data.json', 'r+', encoding='utf-8') as file:
            # Чтение существующих данных
            file_data = json.load(file)
        # Модификация данных (например, добавление нового элемента в список)
        file_data[breed] = new_list
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(file_data, file)
        # Запись обновлённых данных обратно в файл
    else:
        file_data = {}
        with open("data.json", "w", encoding="utf-8") as file:
            file_data[breed] = new_list
            json.dump(file_data, file)

#создаем папку dogs
def create_main_folder(token, path):
    headers = {
        'Authorization' : f'OAuth {token}'
    }
    params = {
        'path' : path
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers = headers, params = params)

def get_pictures_url_subbreed(breed):
    response = get_list_of_subbread(breed)
    types = []
    if response:
        for item in response["message"]:
            url = f'https://dog.ceo/api/breed/{breed}/{item}/images'
            response2 = get_one_picture_subbread(url)
            types.append(response2['message'][0])
    return types

def get_list_of_subbread(breed):
    url = f'https://dog.ceo/api/breed/{breed}/list'
    response = requests.get(url).json()
    return response

def get_one_picture_subbread(url):
    response = requests.get(url).json()
    return response

def get_file_names(types):
    filenames =[]
    for item in types:
        part_url = item.split('/')
        name = part_url[-2] +'_'+ part_url[-1]
        filenames.append(name)
    return filenames

def get_pictures_url_breed(breed):
    types = []
    print('Нет подпород')
    url = f'https://dog.ceo/api/breed/{breed}/images/random/3'
    response = requests.get(url).json()
    for item in response['message']:
        types.append(item)
    return types

breed = input('Введите породу собаки (на английском языке): ')
create_main_folder(token, 'dogs')

subbreed = get_pictures_url_subbreed(breed)
names = get_file_names(subbreed)
if subbreed != []:
    create_internal_folder_yadisk(token, breed)
    counter = 0
    while counter < len(subbreed):
        load_picture_yadisk(subbreed[counter], names[counter], token, breed)
        counter = counter + 1
    write_to_json(subbreed)
else:
    breed_pic = get_pictures_url_breed(breed)
    names = get_file_names(breed_pic)
    create_internal_folder_yadisk(token, breed)
    counter = 0
    while counter < len(breed_pic):
        load_picture_yadisk(breed_pic[counter], names[counter], token, breed)
        counter = counter + 1
    write_to_json(breed_pic)


