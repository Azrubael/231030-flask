WSGI = Web Server Gateway Interfase, стандарт взаимодействия между
Python-программой, выполняюейся на стороне сервера, и самим Web-сервером.


[1] - Установка Python 3.10 или более позднего
# https://docs.python.org/3/using/windows.html#launcher
Установка pip (если нужно)
# https://pip.pypa.io/en/stable/installing/


[2] - Создание изолированой среды
* При работе в Linux
```bash
    $ python3 -m venv az_env
    $ source az_env/bin/activate
```
* При работе в Windows
```bash
    $ py -m venv azwenv
    $ .\azwenv\Scripts\activate
```


[3] - Установка фреймворка Flask и модуля для работы с кастодиальными переменными окружения
```bash
    (az_env)$ pip install Flask
    (az_env)$ pip install python-dotenv
# OR
    (az_env)$ pip install 'python-decouple==3.8'
    
```
OR
```bash
    (az_env)$ pip install -r dependencies.txt
```


[4] - Запуск первого приложения
* При работе в Linux
```bash
    (az_env)$ python3 flask_wsgi_x/flask_wsgi*.py
```
* При работе в Windows
```bash
    (az_env)$ py flask_wsgi_w/flask_wsgi*.py
```


[5] - Создание перечня зависимостей
############ только для разработки ############
```bash
    (az_env)$ pip freeze > dependencies.txt
# OR
    (az_env)$ pip install findpydeps
    (az_env)$ findpydeps -i path/to/folder > dependencies.txt
```


[6] - Деактивация изолированой среды
```bash
    (az_env)$ deactivate
```
