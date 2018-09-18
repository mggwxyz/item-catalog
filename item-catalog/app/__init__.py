# Import flask and template operators
from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify, session as login_session, make_response
import json
from time import sleep
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os

SECRETS_PATH = os.path.abspath(__file__ + '/../../') + '/'
CLIENT_ID = json.loads(open(SECRETS_PATH + 'client_secrets.json', 'r').read())['web']['client_id']
FB_APP_ID = json.loads(open(SECRETS_PATH + 'fb_client_secrets.json', 'r').read())['web']['app_id']

app = Flask(__name__)

app.config.from_object('app.config.DevelopmentConfig')

db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (auth)
from app.auth.controllers import auth
from app.categories.controllers import categories
from app.controllers import main

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(categories)
app.register_blueprint(main)

from app.auth import models
from app.categories import models
from app.items import models

db.drop_all()
db.create_all()

# def initialize_app(script_info=None):
#     # Define the WSGI application object
#     app = Flask(__name__, instance_relative_config=True)
#
#     # Configurations
#     app.config.from_object('app.config.DevelopmentConfig')
#
#     # Define the database object which is imported
#     # by modules and controllers
#     with app.app_context():
#         db.init_app(app)
#         db.drop_all()
#         db.create_all()
#         db.session.commit()
#
#     # Import a module / component using its blueprint handler variable (auth)
#     from app.auth.controllers import auth
#     from app.categories.controllers import categories
#     from app.controllers import main
#
#     # Register blueprints
#     app.register_blueprint(auth)
#     app.register_blueprint(categories)
#     app.register_blueprint(main)
#
#     # shell context for flask cli
#     app.shell_context_processor({'app': app, 'db': db})
#
#     return app
