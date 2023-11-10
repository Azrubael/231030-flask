import datetime
from flask import Flask, render_template, make_response, url_for, \
    request, session
from decouple import config

"""
Общие замечания по применению session.
Принципиально они мало отличаются от cookies. Главная разница заключается в шифровании. Остальные ограничения - такие же, как и для cookies.
Для генерирования качественного секретного ключа рекомендуется использовать встроенные свойства Python:
    $ python3
>>> import os
>>> os.urandom(20).hex()
'22b08beee9de17ab13110a0d196c2301e8ca7b7f'
Такой ключ вполне пригоден для штфрования сессии.
НО!!! Передача сессиронных данных браузеру происходит только в том случае, если состояние объекта session меняется.
Время жизни сессии ограничено непрерывной работой браузера.
По желанию это время можно увеличить до 31 дня, используя параметр
session.permanent = True
Для больше длительности вреени хранения сесси следует использовать
app.permanent_session_lifetime
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.permanent_session_lifetime = datetime.timedelta(days=7)

@app.route("/")
def index():
    if 'visits' in session and isinstance(session['visits'], int | float):
        # увеличение счетчика сессий
        session['visits'] = session.get('visits') + 1
    else:
        # инициализация счетчика сессий
        session['visits'] = 1
    return f"<h3>The Main Page</h3><p>Visits counter: {session['visits']}"


data = [1, 2, 3, 4]
@app.route("/session")
def session_data():
    session.permanent = True        # Признак "перманентной" сессии
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True     # Это для принудительного обновления
    return f"<p>session['data']: {session['data']}"


if __name__ == "__main__":
    app.run(debug=True)