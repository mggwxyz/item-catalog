from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify, session as login_session, make_response
from database import Base, Item, Category
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests



APP = Flask(__name__, template_folder='./templates')

engine = create_engine('sqlite:///item_catalog.db', convert_unicode=True)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@APP.route("/")
@APP.route("/welcome")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    APP.secret_key = 'super_secret_key'
    APP.debug = True
    APP.run(host='0.0.0.0', port=8000)
