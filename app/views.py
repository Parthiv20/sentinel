from app import app


@app.route('/')
def route():
    return "bleek"

@app.route('/index')
def index():
    return "Hello, World!"
