from flask import session as login_session, redirect, flash

def check_login():
    if 'username' not in login_session:
        return redirect('/login')