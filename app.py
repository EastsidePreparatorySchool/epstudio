from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epstudio.db'

#secret key - should be an env variable eventually
app.config['SECRET_KEY'] = "supersecret"

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static/', 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('/', 'sw.js')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')