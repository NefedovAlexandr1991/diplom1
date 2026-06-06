import requests
import os
import json
from settings import token

def to_yadisk(list_types, list_file, token, breed):
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
    headers = {
        'Authorization' : f'OAuth {token}'
    }
    counter = 0
    while counter < len(list_types):
        params = {
            'url' : list_types[counter],
            'path' : f'dogs/{breed}/{list_file[counter]}'
        }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers = headers, params = params)
        if response.ok:
            print(f'Файл {list_file[counter]} загружен')
        else:
            print(f'Файл {list_file[counter]} не загружен')
        counter = counter + 1

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

breed = input('Введите породу собаки (на английском языке): ')
#https://dog.ceo/api/breed/hound/afghan/images картинки всех подвидов
#print(response)
url2 = f'https://dog.ceo/api/breed/{breed}/list'
response2 = requests.get(url2).json()
list_of_types = []
if response2:
    for item in response2["message"]:
        url3 = f'https://dog.ceo/api/breed/{breed}/{item}/images'
        response3 = requests.get(url3).json()
        list_of_types.append(response3['message'][0])
        #print(response3)
#print(list_of_types)
list_of_filenames =[]
for item in list_of_types:
    x = item.split('/')
    y = x[-2] +'_'+ x[-1]
    list_of_filenames.append(y)
#print(list_of_filenames)
#headers = {
    #'Authorization' : f'OAuth {token}'
#}
#params = {
    #'path' : f'dogs/{breed}'
#}
list_of_typesb = []
list_of_filenamesb = []
if not list_of_types:
    print('Нет подпород')
    url = f'https://dog.ceo/api/breed/{breed}/images/random/3'
    response = requests.get(url).json()
    for item in response['message']:
        list_of_typesb.append(item)
    for item in list_of_typesb:
        x = item.split('/')
        y = x[-2] +'_'+ x[-1]
        list_of_filenamesb.append(y)

    to_yadisk(list_of_typesb, list_of_filenamesb, token, breed)
    write_to_json(list_of_typesb)
else:
    to_yadisk(list_of_types, list_of_filenames, token, breed)
    write_to_json(list_of_types)


