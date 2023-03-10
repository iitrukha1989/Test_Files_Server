from configparser import ConfigParser
import requests
import click
import json


def read_config():
    config = ConfigParser()
    config.read('conf.ini')
    return ':'.join([config['socket']['host'], config['socket']['port']])


def convert_code(code_value):
    dict_value = {200: 'OK', 104: 'Not required'}
    return dict_value.get(code_value, 'not OK')


@click.group()
def cli_api():
    pass


@cli_api.command('GET',
                 help="""
                 DESCRIPTION - Получить список файлов/Прочитать файл с сервера и записать на клиента
                 OPTION - socket_value: -p [ip]:[port], default = conf.ini.\n
                 ARGS - name_file: наименование файла который планируем получить от сервера, default =''.\n
                 path_save: абсолютный путь, куда необходимо сохранить файл загруженный из сервера=''.\n
                 NOTE:
                 Если не указать параметр [name_file и path_file] запрос вернет список файлов загруженных на сервере.""")
@click.option('-p', 'socket_value', default=read_config(), show_default=True)
@click.argument('name_file', default='')
@click.argument('path_save', default='')
def GET(socket_value, name_file='', path_save=''):
    socket_value = socket_value.split(':')
    if name_file and path_save:
        res = requests.get(
            f'http://{socket_value[0]}:{socket_value[1]}/download/{name_file}')
        if res.status_code == 200:
            with open(f'{path_save}/{name_file}', 'wb') as tmp_file:
                tmp_file.write(res.content)
                print(convert_code(res.status_code))
        else:
            print(convert_code(res.status_code))
    else:
        res = requests.get(f'http://{socket_value[0]}:{socket_value[1]}/tmp')
        print(json.loads(res.content), convert_code(res.status_code))


@cli_api.command('PUT',
                 help="""
                 DESCRIPTION - Записать файл на сервере.
                 OPTION - socket_value: -p [ip]:[port], default = conf.ini.\n
                 ARGS - name_file: абсолютный путь до файла который планируем загрузить на сервер.\n
                 NOTE:
                 Если не указать/не корректно указать параметр [name_file] запрос вернет код ошибки 400/Not OK""")
@click.option('-p', 'socket_value', default=read_config(), show_default=True)
@click.argument('name_file')
def PUT(socket_value, name_file):
    try:
        with open(name_file, 'rb') as file:
            socket_value = socket_value.split(':')
            res = requests.put(f'http://{socket_value[0]}:{socket_value[1]}/upload',
                               files={'file': file})
            print(convert_code(res.status_code))
    except BaseException:
        print('Не корректно указан файла и/или абсолютный путь до него')


@cli_api.command('POST',
                 help="""
                 DESCRIPTION - Обновить файл на сервере.
                 OPTION - socket_value: -p [ip]:[port], default = conf.ini.\n
                 ARGS - name_file: абсолютный путь до файла который планируем обновить на сервер.\n
                 NOTE:
                 Если не указать/не корректно указать параметр [name_file] запрос вернет код ошибки 400/Not OK.
                 Если файл есть и по hash совпадает - возвращать что не требуется обновление""")
@click.option('-p', 'socket_value', default=read_config(), show_default=True)
@click.argument('name_file')
def POST(socket_value, name_file):
    try:
        with open(name_file, 'rb') as file:
            socket_value = socket_value.split(':')
            res = requests.post(f'http://{socket_value[0]}:{socket_value[1]}/update',
                                files={'file': file})
            print(convert_code(res.status_code))
    except BaseException:
        print('Не корректно указан файла и/или абсолютный путь до него')


@cli_api.command('DELETE',
                 help="""
                 DESCRIPTION - Удалить файл на сервере.
                 OPTION - socket_value: -p [ip]:[port], default = conf.ini.\n
                 ARGS - name_file: наименование файла который планируем удалить на сервере.\n
                 NOTE:
                 Если не указать/не корректно указать параметр [name_file] запрос вернет код ошибки 400/Not OK.
                 Если указанного файла нет на сервере запрос вернет код ошибки 400/Not OK.""")
@click.option('-p', 'socket_value', default=read_config(), show_default=True)
@click.argument('name_file')
def DELETE(socket_value, name_file):
    socket_value = socket_value.split(':')
    res = requests.delete(
        f'http://{socket_value[0]}:{socket_value[1]}/delete/{name_file}')
    print(convert_code(res.status_code))


if __name__ == '__main__':
    cli_api()
