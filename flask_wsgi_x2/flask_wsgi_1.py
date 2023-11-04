from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'refrigerRat0r'

menu = [{"name": "Main", "url": "/"},
        {"name": "Installation", "url": "install-flask"},
        {"name": "First Application", "url": "first-app"},
        {"name": "About", "url": "about"},
        {"name": "Feedback", "url": "contact"}]



@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='The About Page', menu=menu)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        print(f"Message: {request.form['message']}")
        if len(request.form['username']) > 2:
            flash('-= Message sent =-', category='success')
        else:
            flash('-= Sending error =-', category='error')
        
    return render_template('contact.html', title='Feedback', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return  render_template('page404.html', \
            title='Page not found', menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)