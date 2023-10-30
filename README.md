WSGI = Web Server Gateway Interfase, стандарт взаимодействия между
Python-программой, выполняюейся на стороне сервера, и самим Web-сервером.

[1] - Установка Python 3.10 или более позднего
# https://docs.python.org/3/using/windows.html#launcher
Установка pip (если нужно)
# https://pip.pypa.io/en/stable/installing/


[2] - Создание изолированой среды
* При работе в Linux
```bash
    $ python -m venv az_env
    $ source az_env/bin/activate
```
* При работе в Windows
```bash
    $ py -m venv az_env
    $ .\az_env\Scripts\activate
```


[3] - Установка фреймворка Flask
```bash
    (az_env)$ pip install Flask
```

[4] - Запуск первого приложения
```bash
    (az_env)$ python3 flask_wsgi/flask_wsgi_1.py
```

[5] - Деактивация изолированой среды
```bash
    (az_env)$ deactivate
```
