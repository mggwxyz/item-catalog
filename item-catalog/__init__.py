# Import flask and template operators
from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify, session as login_session, make_response
import json
from time import sleep

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Construct client id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Define the database object which is imported
# by modules and controllers
print('connecting to db')
db_status = False
while db_status == False:
    try:
        db = SQLAlchemy(app)
    except:
        sleep(2)
    else:
        print('could not connect')

# Import a module / component using its blueprint handler variable (auth)
from app.auth.controllers import auth
from app.categories.controllers import categories

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(categories)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# App controllers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/welcome")
def index():
    return render_template('index.html')