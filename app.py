# import Flask dependency
from flask import Flask

# create a new Flask app instance
app = Flask(__name__)

# create flask routes
@app.route('/')

# create a hello world function
def hello_world():
    return "Hello World"

