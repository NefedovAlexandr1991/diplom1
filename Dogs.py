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
def create_main_folder(token):
    headers = {
        'Authorization' : f'OAuth {token}'
    }
    params = {
        'path' : 'dogs'
    }
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers = headers, params = params)

def get_pictures_url_subbreed(breed):
    response2 = get_list_of_subbread(breed)
    list_of_types = []
    if response2:
        for item in response2["message"]:
            url3 = f'https://dog.ceo/api/breed/{breed}/{item}/images'
            response3 = get_one_picture_subbread(url3)
            list_of_types.append(response3['message'][0])
    return list_of_types

def get_list_of_subbread(breed):
    url = f'https://dog.ceo/api/breed/{breed}/list'
    response = requests.get(url).json()
    return response

def get_one_picture_subbread(url):
    response = requests.get(url).json()
    return response

def get_file_names(list_of_types):
    list_of_filenames =[]
    for item in list_of_types:
        x = item.split('/')
        y = x[-2] +'_'+ x[-1]
        list_of_filenames.append(y)
    return list_of_filenames

def get_pictures_url_breed(breed):
    list_of_types = []
    print('Нет подпород')
    url = f'https://dog.ceo/api/breed/{breed}/images/random/3'
    response = requests.get(url).json()
    for item in response['message']:
        list_of_types.append(item)
    return list_of_types

breed = input('Введите породу собаки (на английском языке): ')
create_main_folder(token)

list_of_subbreed = get_pictures_url_subbreed(breed)
names_of_subbreed = get_file_names(list_of_subbreed)
if list_of_subbreed != []:
    create_internal_folder_yadisk(token, breed)
    counter = 0
    while counter < len(list_of_subbreed):
        load_picture_yadisk(list_of_subbreed[counter], names_of_subbreed[counter], token, breed)
        counter = counter + 1
    write_to_json(list_of_subbreed)
else:
    list_of_breed = get_pictures_url_breed(breed)
    names_of_breed = get_file_names(list_of_breed)
    create_internal_folder_yadisk(token, breed)
    counter = 0
    while counter < len(list_of_breed):
        load_picture_yadisk(list_of_breed[counter], names_of_breed[counter], token, breed)
        counter = counter + 1
    write_to_json(list_of_breed)


