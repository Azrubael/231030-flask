from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"name": "Main", "url": "/"},
        {"name": "Add post", "url": "/add_post"},
        {"name": "Img", "url": "/show_img"},
        {"name": "About", "url": "/about"}]


@app.route("/")
def index():
    return render_template("index.html", menu=menu)


@app.route('/about')
def about():
    content = render_template("about.html", title='The About Page', \
                            menu=menu, posts=[])
    res = make_response(content)
    res.headers["Content-Type"] = "text/plain"
    res.headers["Server"] = "flasksite"
    return res


@app.route('/show_img')
def show_img():
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


@app.errorhandler(404)
def page_not_found(error):
    return make_response("<h3>Server error</h3>", 500)


if __name__ == "__main__":
    app.run(debug=True)

# Flask_11_ timecode [06:30]