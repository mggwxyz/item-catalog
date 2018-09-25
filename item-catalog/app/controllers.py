from flask import Blueprint, session as login_session, render_template, redirect
from app.auth.util import login_required

main = Blueprint('main', __name__)


# App controllers
@main.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@main.route("/")
@login_required
def index():
    return redirect('/dashboard')


@main.route("/dashboard")
@login_required
def dashboard():
    print(login_session)
    return render_template('dashboard.html', login_session=login_session)
