from flask import Flask, render_template, make_response, redirect, url_for

# Flask_11_
app = Flask(__name__)

menu = [{"name": "Main", "url": "/"},
        {"name": "Add post", "url": "/add_post"},
        {"name": "Img", "url": "/show_img"},
        {"name": "Txt", "url": "/show_plaintext"},
        {"name": "Moved", "url": "/transfer"},
        {"name": "About", "url": "/about"}]


@app.route("/")
def index():
    """Рендеринг гдавной страницы без каких-либо особенностей."""
    return render_template("index.html", menu=menu)


@app.route('/about')
def about():
    """Рендеринг страницы отключен, вывоится необработанный текст."""
    content = render_template("about.html", title='The About Page', \
                            menu=menu, posts=[])
    res = make_response(content)
    res.headers["Content-Type"] = "text/plain"
    res.headers["Server"] = "flasksite"
    return res


@app.route('/show_img')
def show_img():
    """Пример вывода изображения."""
    img = None
    with app.open_resource( app.root_path + "/static/pic/a11vo.jpg", \
                           mode="rb") as f:
        img = f.read()
    if img is None:
        return "None image"
    res = make_response(img)
    res.headers["Content-Type"] = "image/jpg"
    res.headers["Server"] = "flasksite"
    return res


@app.route("/show_plaintext")
def show_plaintext():
    """Вывод простого необработанного текста и передача кода ответа сервера."""
    return "<h1>Some interesting plaint text...</h1>", 200, \
        {"Content-type": "text/plain"}


@app.errorhandler(404)
def page_not_found(error):
    """Простой рендеринг ошибки и передача кастомного ответа сервера."""
    return make_response("<h3>Server error</h3>", 500)


@app.route("/transfer")
def transfer():
    """Пример перенаправления на другой постоянный URL-адрес."""
    return redirect( url_for("show_img"), 301 )
# 301 - Страница перемещена на другой постоянный URL-адрес
# 302 - Страница перемещена временно на другой URL-адрес


if __name__ == "__main__":
    app.run(debug=True)

