from flask import Flask, render_template, session, redirect, url_for
from auth import auth
from student import get_all_students, add_student

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
        
@app.route("/schueler")
def schueler():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("students.html", schueler=get_all_students())
    
@app.route("/add", methods=["GET", "POST"])
def add():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        name = request.form["name"]
        progress = request.form["progress"]
        add_student(name, progress)
        return redirect(url_for('schueler'))

    return render_template("add.html")

@app.route("/diagrammkarte")
def diagrammkarte():
    return render_template("diagrammkarte.html")
