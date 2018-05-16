from flask import Blueprint, session as login_session, render_template, redirect

main = Blueprint('main', __name__)

# App controllers
@main.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@main.route("/")
@main.route("/welcome")
def index():
    return render_template('index.html')