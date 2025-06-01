from flask import Flask, render_template, request, redirect, url_for, session
from auth import auth
from student import get_all_students, add_student
from storage import save_diagrammkarte

app = Flask(__name__)
app.secret_key = "supergeheim"  # Wichtig für Login-Sessions

# Login-Blueprint registrieren
app.register_blueprint(auth)

# ========== ROUTE: STARTSEITE ==========
@app.route("/start")
def start():
    if "user" in session:
        return render_template("start.html")
    else:
        return redirect(url_for("auth.login"))

# ========== ROUTE: SCHÜLERÜBERSICHT ==========
@app.route("/schueler")
def schueler():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("students.html", schueler=get_all_students())

# ========== ROUTE: NEUEN SCHÜLER HINZUFÜGEN ==========
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name")
        progress = request.form.get("progress")
        add_student(name, progress)
        return redirect(url_for("schueler"))

    return render_template("add.html")

# ========== ROUTE: AUSBILDUNGSDIAGRAMMKARTE ==========
@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "vorname": request.form.get("vorname"),
            "anlage": request.form.get("anlage"),
            "grundstufe": [key for key in request.form.keys() if key.startswith("grund_")],
            "aufbaustufe": [key for key in request.form.keys() if key.startswith("aufbau_")],
            "leistungsstufe": [key for key in request.form.keys() if key.startswith("leistung_")]
        }

        save_diagrammkarte(data)
        return render_template("diagrammkarte.html", status="✅ Daten gespeichert")

    return render_template("diagrammkarte.html")


# ========== ROUTE: GELESENE DATEI ANZEIGEN ==========
@app.route("/saved")
def show_saved():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return render_template("anzeigen.html", daten=content)
    except FileNotFoundError:
        return render_template("anzeigen.html", daten="❌ Noch keine Eintragung vorhanden.")


# ========== START DER APP (lokal) ==========
if __name__ == "__main__":
    app.run(debug=True)
