from flask import Flask, render_template, session, redirect, url_for
from auth import auth
from student import get_all_students, add_student
from storage import save_diagrammkarte
from storage import save_diagrammkarte

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

        print("Schülerdaten gespeichert:")
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

from storage import save_diagrammkarte

@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "vorname": request.form.get("vorname"),
            "anlage": request.form.get("anlage"),
            "grundstufe": [
                key for key in request.form.keys()
                if key.startswith("grund_")
            ],
            "aufbaustufe": [
                key for key in request.form.keys()
                if key.startswith("aufbau_")
            ],
            "leistungsstufe": [
                key for key in request.form.keys()
                if key.startswith("leistung_")
            ]
        }

        save_diagrammkarte(data)  # Speichern in Datei
        return redirect(url_for("diagrammkarte"))

    return render_template("diagrammkarte.html")

@app.route("/saved")
def show_saved():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return "Noch keine Eintragungen vorhanden."

@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        save_diagrammkarte(form_data)
        return "Daten gespeichert ✅"

    return render_template("diagrammkarte.html")
