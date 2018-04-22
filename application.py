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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APP = Flask(__name__, template_folder='./templates')

engine = create_engine('sqlite:///item_catalog.db', convert_unicode=True)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


@APP.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@APP.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Grab the authorization code
    code = request.data

    try:
        # Upgrade authorization code into credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.', 401))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token, login is aborted
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.header['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if this user is connected already
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@APP.route('/gdisconnect')
def gdisconnect():
    # Grab access token from login session
    access_token = login_session.get('access_token')

    # Check to see if they currently have a access token
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Print out access token and user to be disconncted
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])

    # Send a request to revoke the user's access token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)

    # If the request to revoke the access token was successful
    if result['status'] == '200':
        # Clear the user's session
        del(login_session['access_token'])
        del(login_session['gplus_id'])
        del(login_session['username'])
        del(login_session['email'])
        del(login_session['picture'])

        # Return response indicating successful disconnect
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If the disconnect was unsuccessful
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@APP.route("/")
@APP.route("/welcome")
def index():
    return render_template('index.html')


@APP.route("/categories")
def view_all_categories():
    all_categories = session.query(Category)
    return render_template('categories.html', categories=all_categories)


@APP.route("/api/categories")
def view_all_categories_api():
    all_categories = session.query(Category)
    return jsonify(categories=[i.serialize for i in all_categories])


@APP.route("/categories/new/", methods=['GET', 'POST'])
def create_new_category():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        name = name = request.form['name']
        description = request.form['description']
        new_category = Category(name=name, description=description)
        session.add(new_category)
        session.flush()
        session.commit()
        flash('New category #' + name + ' was created')
        return redirect(url_for('view_all_categories'))
    return render_template('new-category.html')


@APP.route("/categories/<int:category_id>/")
def view_category(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('view-category.html', category=category)


@APP.route("/api/categories/<int:category_id>/")
def view_category_api(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return jsonify(category=category.serialize)


@APP.route("/categories/<int:category_id>/edit/")
def edit_category(category_id):
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('edit-category.html', category=category)


@APP.route("/categories/<int:category_id>/delete/", methods=['GET', 'POST'])
def delete_category(category_id):
    if request.method == 'POST':
        if 'yes' in request.form:
            results_query = session.query(Category)
            results = results_query.filter(Category.id == category_id)
            category = results.first()
            session.delete(category)
            session.commit()
            return redirect(url_for('view_all_categories'))
        return redirect(url_for('view_category', category_id=category_id))
    results = session.query(Category).filter(Category.id == category_id)
    category = results.first()
    return render_template('delete-category.html', category=category)


if __name__ == '__main__':
    APP.secret_key = 'super_secret_key'
    APP.debug = True
    APP.run(host='0.0.0.0', port=8000)
