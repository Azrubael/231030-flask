from flask import Flask, render_template

app = Flask(__name__)

menu = ["Installation", "First Application", "Feedback"]

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='The Main Page', menu=menu)
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)