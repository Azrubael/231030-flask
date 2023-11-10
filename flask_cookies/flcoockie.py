from flask import Flask, render_template, make_response, url_for, request

"""
Общие замечания по применению куки.
[1] Куки небезопасны, ивсе данные, которые туда попадают, доступны для всех пользователей. Их можно в том числе просматривать. Кроме того, в большинстве браузеров куки можно отключать. В этом случае данные в них сохраняться не будут, а сервер об этом даже не будет знать.
[2] Для проверки включения куки может использоваться JavaScript:
<script>
    document.cookie="ex=1;"
    if (!document.cookie) {
        alert("Эта страница для корректной работы требует включения cookies.");
    }
</script>
[3] Для cookie имеюется огранияениеЖ 4Кб на каждый ключ.
[4] Количество доступных для cookie ключей может отличаться, в зависимости от браузера, от 30 до 50 ключей.
[5] Куки добавляются к каждому запросу на сервер. Поэтому не стоит ими злоупотреблять.
"""

app = Flask(__name__)

menu = [{"name": "Main", "url": "/"},
        {"name": "About", "url": "/about"},
        {"name": "Login", "url": "/login"},
        {"name": "Logout", "url": "/logout"}]


@app.route("/")
def index():
    return render_template("index.html", menu=menu)


@app.route('/about')
def about():
    return "<h3>The About Page</h3>"


@app.route("/login")
def login():
    log =""
    if request.cookies.get("logged"):
        log = request.cookies.get("logged")

    res = make_response(f"<h3>The Authorization Form</h3><p>logged: {log}")
    res.set_cookie("logged", "yes", 24*3600)    # для хранения куки 24 часа
    return res


@app.route("/logout")
def logout():
    res = make_response("<p>You aren't logged in!<p>")
    res.set_cookie("logged", "", 0)             # для немедленого удаления куки
    return res


if __name__ == "__main__":
    app.run(debug=True)