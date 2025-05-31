from flask import Blueprint, render_template, request, redirect, url_for, session

auth = Blueprint('auth', __name__)

USERNAME = "admin"
PASSWORD = "1234"

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['user'] = USERNAME
            return redirect(url_for('start'))
        else:
            return "Falsche Zugangsdaten"
    return render_template('login.html')
