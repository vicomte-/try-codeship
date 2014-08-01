from red import app

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/hello/<name>')
def hi(name):
    return 'Hello %s!' % name
