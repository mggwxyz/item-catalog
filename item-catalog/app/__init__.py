# import flask and template operators
from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify, session as login_session, make_response
import json
from time import sleep
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

import sys

print(sys.executable)

SECRETS_PATH = os.path.abspath(__file__ + '/../../') + '/'
CLIENT_ID = json.loads(open(SECRETS_PATH + 'client_secrets.json', 'r').read())['web']['client_id']
fb_app_id = json.loads(open(SECRETS_PATH + 'fb_client_secrets.json', 'r').read())['web']['app_id']

app = Flask(__name__)

app.config.from_object('app.config.DevelopmentConfig')

db = SQLAlchemy(app)

# import a module / component using its blueprint handler variable (auth)
from app.auth.controllers import auth
from app.categories.controllers import categories
from app.controllers import main

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(categories)
app.register_blueprint(main)

from app.auth import models
from app.categories import models
from app.items import models

db.drop_all()
db.create_all()

# def initialize_app(script_info=none):
#     # define the wsgi application object
#     app = flask(__name__, instance_relative_config=true)
#
#     # configurations
#     app.config.from_object('app.config.developmentconfig')
#
#     # define the database object which is imported
#     # by modules and controllers
#     with app.app_context():
#         db.init_app(app)
#         db.drop_all()
#         db.create_all()
#         db.session.commit()
#
#     # import a module / component using its blueprint handler variable (auth)
#     from app.auth.controllers import auth
#     from app.categories.controllers import categories
#     from app.controllers import main
#
#     # register blueprints
#     app.register_blueprint(auth)
#     app.register_blueprint(categories)
#     app.register_blueprint(main)
#
#     # shell context for flask cli
#     app.shell_context_processor({'app': app, 'db': db})
#
#     return app
