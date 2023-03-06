from configparser import ConfigParser
from os import system, name
import requests
import json
import sys


# Основные функции клиентской части/API по условию тестового задания:
# 1. Получить список файлов
def get_list(socket_value):
    res = requests.get(f'http://{socket_value[0]}:{socket_value[1]}/tmp')
    print(json.loads(res.content), convert_code(res.status_code))


# 2. Прочитать файл с сервера и записать на клиента
def get_file(name_file, dir_path, socket_value):
    res = requests.get(
        f'http://{socket_value[0]}:{socket_value[1]}/download/{name_file}')
    if res.status_code == 200:
        with open(f'{dir_path}/{name_file}', 'wb') as tmp_file:
            tmp_file.write(res.content)
            print(convert_code(res.status_code))
    else:
        print(convert_code(res.status_code))


# 3. Записать на сервер файл.
def send_file(name_file, socket_value):
    try:
        with open(name_file, 'rb') as file:
            res = requests.put(f'http://{socket_value[0]}:{socket_value[1]}/upload',
                               files={'file': file})
            print(convert_code(res.status_code))
    except:
        print('Не корректно указан файла и/или абсолютный путь до него')


# 4. Обновить на сервере файл
def update_file(name_file, socket_value):
    try:
        with open(name_file, 'rb') as file:
            res = requests.post(f'http://{socket_value[0]}:{socket_value[1]}/update',
                                files={'file': file})
            print(convert_code(res.status_code))
    except:
        print('Не корректно указан файла и/или абсолютный путь до него')


# 5. Удалить на сервере файл.
def deleta_file(name_file, socket_value):
    res = requests.delete(
        f'http://{socket_value[0]}:{socket_value[1]}/delete/{name_file}')
    print(convert_code(res.status_code))


# Опционные (дополнительные функции) для корректной работы клиентской части/API
# 1. Проверка наличия соединения между сервером и клиентом
def check_connect(socket_value):
    try:
        return requests.get(f'http://{socket_value[0]}:{socket_value[1]}/tmp').status_code
    except:
        return 400


# 2. Опционный вывов меню программы
def output_option_1():
    print('''Выбирите один из пунктов меню:
    1. Получить список файлов.
    2. Прочитать файл с сервера и записать на клиента.
    3. Записать на сервер файл.
    4. Обновить на сервере файл.
    5. Удалить на сервере файл.
    6. Закрыть соединение с сервером''')


# 3. Опционный вывов меню программы
def output_option_2():
    print('''Продолжить работу с сервером
    1. Да
    2. Нет''')


# 4. Преобразование кода ответа HTTP
def convert_code(code_value):
    dict_value = {200: 'OK', 104: 'Not required'}
    return dict_value.get(code_value, 'not OK')


# 5. Опционная функция проверка валидности данных из командной строки
def validation_data(tmp_value, option_value):
    if option_value == 7:
        clear()
        output_option_1()
    else:
        clear()
        output_option_2()
    if check_digit(tmp_value) is False:
        return validation_data(input(), option_value=option_value)
    else:
        if int(tmp_value) not in range(1, option_value):
            return validation_data(input(), option_value=option_value)
        else:
            return tmp_value


# 6. Опционная функция проверка валидности данных из командной строки
def check_digit(tmp_value):
    try:
        str(tmp_value).isdigit()
        (isinstance(int(tmp_value), int))
        return True
    except:
        return False


# 7. Очистка терминала
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# 8. Основная функция CLI для работы клиентской части/API
def option_main(socket_value):
    while (True):
        output_option_1()
        number_value = validation_data(input(), option_value=7)
        if int(number_value) == 6:
            print('Соединение с сервером закрыто')
            break
        else:
            match int(number_value):
                case 1:
                    get_list(socket_value=socket_value)
                case 2:
                    print(
                        'Укажите наименования файла и директиву для сохранения, через пробел')
                    try:
                        name_file, dir_path = input().split()
                        get_file(name_file=name_file, dir_path=dir_path,
                                 socket_value=socket_value)
                    except:
                        print(
                            'Не корректно указан файла и/или абсолютный путь до него')
                case 3:
                    print('Укажите полный путь до файла для записи на сервер')
                    send_file(name_file=input(), socket_value=socket_value)
                case 4:
                    print('Укажите полный путь до файла для обновления на сервер')
                    update_file(name_file=input(), socket_value=socket_value)
                case 5:
                    print(
                        'Укажите наименования файла который необходимо удалить на сервере')
                    deleta_file(name_file=input(), socket_value=socket_value)
            output_option_2()
            number_value = validation_data(input(), option_value=3)
            if int(number_value) == 2:
                break
            clear()


# Основная функция, проверка аргументов командной строки, запуск основных и дополнительных функций
def main(argv_value):
    if len(argv_value) == 1:
        config = ConfigParser()
        config.read('conf.ini')
        socket_value = [config['socket']['host'], config['socket']['port']]
    else:
        socket_value = [argv_value[1], argv_value[2]]
    clear()
    print('Добрый день!')
    if check_connect(socket_value) != 200:
        print('Ошибка, сервер не доступен, проверьте настройки сервера и клиента')
    else:
        option_main(socket_value)


if __name__ == '__main__':
    main(sys.argv)
