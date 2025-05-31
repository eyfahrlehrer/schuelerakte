from flask import Flask, render_template, session, redirect, url_for
from auth import auth
from student import get_all_students, add_student

app = Flask(__name__)
app.secret_key = "supergeheim"  # wichtig für Login-Sessions

# Blueprint für Login verwenden
app.register_blueprint(auth)

@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if request.method == "POST":
        name = request.form.get("name")
        vorname = request.form.get("vorname")
        anlage = request.form.get("anlage")
        grund = request.form.getlist("grund")
        aufbau = request.form.getlist("aufbau")
        leistung = request.form.getlist("leistung")

        print("📋 Schülerdaten gespeichert:")
        print("Name:", name)
        print("Vorname:", vorname)
        print("Anlage-Nr.:", anlage)
        print("Grundstufe:", grund)
        print("Aufbaustufe:", aufbau)
        print("Leistungsstufe:", leistung)

    return render_template("diagrammkarte.html")

        
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
