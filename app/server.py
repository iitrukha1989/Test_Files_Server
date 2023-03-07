from flask import Flask, request, send_file, Response
from pathlib import Path
import hashlib
import json
import os

APP_DIR = str(Path.cwd())[:str(Path.cwd()).rfind('/')]

app_server = Flask(__name__)
app_server.config.from_object(__name__)


# Основные функции серверной части по условию тестового задания:
# 1. Получить список файлов
@app_server.route('/tmp', methods=['GET'])
def show_item():
    if request.method == 'GET':
        res_list = list()
        for tmp_file in os.listdir(f'{APP_DIR}/tmp'):
            res_list.append((tmp_file, hash_function(tmp_file)))
        return json.dumps(res_list)


# 2. Прочитать файл с сервера и записать на клиента
@app_server.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    if request.method == 'GET':
        if file_name in os.listdir(f'{APP_DIR}/tmp'):
            return send_file(os.path.join(f'{APP_DIR}/tmp', file_name))
        else:
            return Response(status=400)


# 3. Записать на сервер файл.
@app_server.route('/upload', methods=['PUT'])
def upload_file():
    if request.method == "PUT":
        file = request.files['file']
        file.save(f'{APP_DIR}/tmp/{file.filename}')
        return Response(status=200)


# 4. Обновить на сервере файл
@app_server.route('/update', methods=['POST'])
def update_file():
    if request.method == 'POST':
        file = request.files['file']
        for tmp_file in os.listdir(f'{APP_DIR}/tmp'):
            if tmp_file == file.filename:
                if hash_function(tmp_file) != hash_function(file.filename):
                    file.save(f'{APP_DIR}/tmp/{file.filename}')
                    return Response(status=200)
                else:
                    return Response(status=104)


# 5. Удалить на сервере файл.
@ app_server.route('/delete/<file_name>', methods=['DELETE'])
def delete_file(file_name):
    if request.method == 'DELETE':
        if file_name in os.listdir(f'{APP_DIR}/tmp'):
            os.remove(os.path.join(f'{APP_DIR}/tmp', file_name))
            return Response(status=200)
        else:
            return Response(status=400)


# Опционные (дополнительные функции) для серверной части
# 1. Вычисление hash-суммы по наименованию файла
def hash_function(file_name):
    with open(f'{APP_DIR}/tmp/{file_name}', 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


if __name__ == '__main__':
    app_server.run(debug=True, host='0.0.0.0', port='8000')
