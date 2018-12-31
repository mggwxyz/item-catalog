from flask import session, redirect, url_for, flash
from functools import wraps


def check_login():
    if 'username' not in session:
        return redirect(url_for('auth.show_login'))

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(session)
        if 'user_id' in session:
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('auth.show_login'))
    return wrapper