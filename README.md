# Test_Files_Server

Тестовое задания по разработке файлового сервера и CLI - приложения. 

Приложение разработано на языке Python с использованием фреймворка Flask. 

## Структура проекта:

```
File_server_test_app
├── app
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
├── client.py
├── client_v2.py
├── compose.yaml
├── conf.ini
├── test_cli.py
└── tmp
```

## Порядок запуска проекта
1. Запускается образ, с помощью утилиты docker compose
2. Запуск тестов pytest
3. Запуск CLI - приложения с помощью client_v2.py \
   Дополнительно имеется возможность запустить интерактивную версию CLI - приложения с помощью client.py


## Сборка и запуск образа с помощью **docker compose** и следующих команд:
```
docker-compose build
docker-compose up -d
docker run -p 8001:8000 [*название образа - можно посмотреть с помощью команды docker images]
```
Пример вызова команды docker images. 
```
File_server_test_app docker images       
REPOSITORY                 TAG       IMAGE ID       CREATED       SIZE
file_server_test_app-web   latest    5e2f9f7ba2e1   9 hours ago   80.1MB
```

## Запуск тестов pytest
Для запуска тестирования CLI - приложения достаточно запустить команду **pytest [-v]** или **pytest [-v] test_cli.py.** \
Без аргумента pytest исследует весь текущий каталог и все его подкаталоги, для поиска и запуска тестовых файлов и тестовых функций. \
В файле **test_cli.py** реализовано 14 тестовых функций по всем возможным командам client_v2 [GET, PUT, POST, DELETE], с использованием и без использования дополнительных опций и параметров. \
Подробно с опциями и параметрами можно ознакомиться в следующем разделе. 

Ожидаемый результаты запуска тестов:
```
======================== test session starts =========================
platform darwin -- Python 3.10.6, pytest-7.2.0, pluggy-1.0.0 -- /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /fake_path/File_server_test_app
plugins: anyio-3.6.2
collected 14 items                                                   

test_cli.py::test_get_1 PASSED                                 [  7%]
test_cli.py::test_get_2 PASSED                                 [ 14%]
test_cli.py::test_put_1 PASSED                                 [ 21%]
test_cli.py::test_put_2 PASSED                                 [ 28%]
test_cli.py::test_get_3 PASSED                                 [ 35%]
test_cli.py::test_get_4 PASSED                                 [ 42%]
test_cli.py::test_get_5 PASSED                                 [ 50%]
test_cli.py::test_get_6 PASSED                                 [ 57%]
test_cli.py::test_post_1 PASSED                                [ 64%]
test_cli.py::test_post_2 PASSED                                [ 71%]
test_cli.py::test_delete_1 PASSED                              [ 78%]
test_cli.py::test_put_3 PASSED                                 [ 85%]
test_cli.py::test_delete_2 PASSED                              [ 92%]
test_cli.py::test_get_7 PASSED                                 [100%]

========================= 14 passed in 0.17s =========================
```

## CLI - Приложения:
### 1. client_v2. 
Обновленная версия CLI - Приложения, которая использует **click** для создания интерфейса.
После успешной сборки образа можно запустить CLI - приложения **client_v2.py**. \
Программа использует **click** для создания интерфейса.
При вызове команд: python3 client_v2.py --help или python3 client_v2.py выводиться справочная информация с какими опциями и параметрами можно запускать данную программу.

Пример вызова команды **python3 client_v2.py --help**:

```
Usage: client_v2.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  DELETE  DESCRIPTION - Удалить файл на сервере.
  GET     DESCRIPTION - Получить список файлов/Прочитать файл с...
  POST    DESCRIPTION - Обновить файл на сервере.
  PUT     DESCRIPTION - Записать файл на сервере.
```
Дополнительно имеется возможность выгрузить справочную информацию отдельно по каждой команде: python3 client_v2.py [GET, PUT, POST, DELETE] --help, со списком опций и параметров для каждой команды отдельно.

Примеры вызова команд client_v2.py:
```
python3 client_v2.py GET
python3 client_v2.py GET -p [ip:port]
python3 client_v2.py PUT [абослютный путь до файла]/test_1.txt
python3 client_v2.py POST -p [ip:port] [абослютный путь до файла]/test_1.txt
python3 client_v2.py GET -p [ip:port] test_1.txt [абсолютный путь куда необходимо сохранить файл]
```

### 2. client_v1.
Интерактивная версия CLI - Приложения, без использования сторонних модулей. \
Запуск скрипт возможен с параметрами и без:
- Запуск без параметров **python3 client.py**, в этом случае сокет (пара ip-адреса и порта) будут взяты из файла **conf.ini** 
- Запуск с параметрами в этом случае необходимо указать сокет в командной строки, например **python3 client.py 127.0.0.1 8000**

После запуска происходит автоматическая проверка доступности сервера. \
В случае если подключение к серверу будет не доступно териминал выдаст сообщение:
- Ошибка, сервер не доступен, проверьте настройки сервера и клиента

В этом случае необходимо проверить:
- Запущен ли сервер и с какими настройками
- Использовать другой сокет для подключения

После успешного запуск **client.py** в терминале будет доступно основное меню программы. 

### Основное меню приложения

Основное меню приложения имеет следующий вид. \
Выбор каждого пункта происходит через ввода цифры соответсвующего пункта меню.

```
Выбирите один из пунктов меню:
    1. Получить список файлов.
    2. Прочитать файл с сервера и записать на клиента.
    3. Записать на сервер файл.
    4. Обновить на сервере файл.
    5. Удалить на сервере файл.
    6. Закрыть соединение с сервером
```
    
Все пункту кроме 1, после выбора запрашивают уточняющую информацию. \
После отработки пункта происходит автоматических вывоз дополнительного меню где пользователю предлогают завершить или продолжить CLI - программу

### Дополнительное меню приложения:

Дополнительное меню приложения имеет следующий вид. \
Выбор каждого пункта происходит через ввода цифры соответсвующего пункта меню.
```
Продолжить работу с сервером
    1. Да
    2. Нет
```
