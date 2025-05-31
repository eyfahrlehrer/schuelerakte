from flask import Flask, render_template, session, redirect, url_for
from auth import auth

app = Flask(__name__)
app.secret_key = "supergeheim"  # wichtig für Login-Sessions

# Blueprint für Login verwenden
app.register_blueprint(auth)

@app.route('/start')
def start():
    if 'user' in session:
        return render_template('start.html')
    else:
        return redirect(url_for('auth.login'))
