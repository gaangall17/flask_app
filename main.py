from flask import Flask

app = Flask(__name__)

@app.route('/')   #url root where function hello() would run
def hello():
    return 'Hello World Flask'