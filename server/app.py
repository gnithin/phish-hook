from flask import Flask
app = Flask(__name__)

@app.route('/detect')
def hello_world():
    return 'hi!'
