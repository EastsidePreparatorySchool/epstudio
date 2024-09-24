from flask import Flask

test = Flask(__name__) # needs to match file name

@test.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

# put these lines in the terminal then click on link to open webpage
# set FLASK_APP=test
# set FLASK_ENV=development
# flask run