from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = ["Installation", "First Application", "Feedback"]

@app.route('/index')
@app.route('/')
def index():
    print( url_for('index') )
    return render_template('index.html', menu=menu)
    
@app.route('/about')
def about():
    print( url_for('about') )
    return render_template('about.html', title='The About Page', menu=menu)

@app.route("/profile/<username>")
def profile(username):
    """После ввода в сроке адреса http://127.0.0.1:5000/profile/az
    выводит надпись 'User: az'."""
    return f"User: {username}"

@app.route("/useful_app/<path:username>")
def useful_app(username):
    """После ввода в сроке адреса http://127.0.0.1:5000/profile/az/longpath
    выводит надпись 'User: az/longpath'."""
    return f"User: {username}"

@app.route("/uapp/<int:username>/<path>")
def uapp(username, path):
    """После ввода в сроке адреса http://127.0.0.1:5000/profile/324/somebody
    выводит надпись 'User: 324, somebody'."""
    return f"User: {username}, {path}"

# Тестовый запрос для проверки работы контекстов без запуска вебсервера
# with app.test_request_context():
#     print( url_for('index') )
#     print( url_for('about') )
#     print( url_for('profile', username="az") )
#     print( url_for('useful_app', username="az/longpath") )


if __name__ == '__main__':
    app.run(debug=True)