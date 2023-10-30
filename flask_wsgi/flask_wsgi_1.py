from flask import Flask

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>The Main Page</title>
</head>
<body>
    <h3>The Main Page</h3>
</body>
</html>
'''
    
@app.route('/about')
def about():
    return '<h1>About the Site</h1>'

if __name__ == '__main__':
    app.run(debug=True)