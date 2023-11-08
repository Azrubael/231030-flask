from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"name": "Main", "url": "/"},
        {"name": "Add post", "url": "/add_post"},
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


@app.errorhandler(404)
def page_not_found(error):
    return  render_template('page404.html', \
            title='Page not found', menu=menu), 404


if __name__ == "__main__":
    app.run(debug=True)