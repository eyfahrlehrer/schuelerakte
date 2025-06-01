from flask import Flask, render_template, request, redirect, url_for, session, send_file
import io
from xhtml2pdf import pisa
from storage import save_diagrammkarte

app = Flask(__name__)
app.secret_key = "geheimcode123"

# Dummy-Login-Daten
users = {
    "admin": "passwort"
}

# Route: Startseite mit Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("diagrammkarte"))
        else:
            return render_template("login.html", fehler="❌ Falscher Benutzername oder Passwort.")
    return render_template("login.html")

# Route: Ausbildungsdiagrammkarte anzeigen und speichern
@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "vorname": request.form.get("vorname"),
            "anlage": request.form.get("anlage"),
            "grundstufe": [key for key in request.form if key.startswith("grund_")],
            "aufbaustufe": [key for key in request.form if key.startswith("aufbau_")],
            "leistungsstufe": [key for key in request.form if key.startswith("leistung_")]
        }
        save_diagrammkarte(data)
        return render_template("diagrammkarte.html", status="✅ Daten gespeichert")

    return render_template("diagrammkarte.html")

@app.route("/stammdaten", methods=["GET", "POST"])
def stammdaten():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        session["stammdaten"] = {
            "name": request.form.get("name"),
            "vorname": request.form.get("vorname"),
            "geburtsdatum": request.form.get("geburtsdatum"),
            "strasse": request.form.get("strasse"),
            "hausnummer": request.form.get("hausnummer"),
            "mobil": request.form.get("mobil"),
            "sehhilfe": "sehhilfe" in request.form,
            "theorie_bestaanden": "theorie_bestaanden" in request.form
        }
        return redirect(url_for("grundstufe"))

    return render_template("stammdaten.html")

@app.route("/grundstufe", methods=["GET", "POST"])
def grundstufe():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = {
            "stammdaten": session.get("stammdaten", {}),
            "grundstufe": {
                "einsteigen": "einsteigen" in request.form,
                "sitz": "sitz" in request.form,
                "lenkrad": "lenkrad" in request.form,
                "spiegel": "spiegel" in request.form,
                "kopfstuetze": "kopfstuetze" in request.form,
                "lenkhaltung": "lenkhaltung" in request.form,
                "pedale": "pedale" in request.form,
                "guert": "guert" in request.form,
                "wahlhebel": "wahlhebel" in request.form,
                "zuendschloss": "zuendschloss" in request.form,
                "motor": "motor" in request.form,
                "anhalteuebungen": "anhalteuebungen" in request.form,
                "lenkuebungen": "lenkuebungen" in request.form,
                "hoch": [key for key in request.form if key.startswith("hoch_")],
                "runter": [key for key in request.form if key.startswith("runter_")],
                "notizen": request.form.get("notizen")
            }
        }

        # Speichern in Datei
        with open("saved_grundstufe.txt", "a", encoding="utf-8") as f:
            f.write(str(eintrag) + "\\n")

        return render_template("grundstufe.html", status="✅ Grundstufe gespeichert")

    return render_template("grundstufe.html")

@app.route("/aufbaustufe", methods=["GET", "POST"])
def aufbaustufe():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = {
            "stammdaten": session.get("stammdaten", {}),
            "aufbaustufe": {
                "rollen": "rollen" in request.form,
                "abbremsen": "abbremsen" in request.form,
                "bremsuebungen": {
                    "degressiv": "brems_degressiv" in request.form,
                    "zielbremsung": "brems_ziel" in request.form,
                    "gefahr": "brems_gefahr" in request.form
                },
                "gefaelle": {
                    "anhalten": "g_anh" in request.form,
                    "anfahren": "g_anf" in request.form,
                    "rueckwaerts": "g_rueck" in request.form,
                    "sichern": "g_sichern" in request.form,
                    "schalten": "g_schalten" in request.form
                },
                "tastgeschwindigkeit": "tastgeschwindigkeit" in request.form,
                "kontrolleinrichtungen": "kontrolleinrichtungen" in request.form,
                "besonderheiten": "besonderheiten" in request.form,
                "notizen": request.form.get("notizen")
            }
        }

        # Speichern in Datei
        os.makedirs("db", exist_ok=True)
        with open("db/saved_aufbaustufe.txt", "a", encoding="utf-8") as f:
            f.write(str(eintrag) + "\n")

        return render_template("aufbaustufe.html", status="✅ Aufbaustufe gespeichert")

    return render_template("aufbaustufe.html")


# Route: Gespeicherte Daten anzeigen
@app.route("/anzeigen")
def anzeigen():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            daten = f.readlines()
    except FileNotFoundError:
        return render_template("anzeigen.html", fehler="Noch keine Einträge vorhanden.")

    return render_template("anzeigen.html", eintraege=daten)

# Route: PDF-Export der gespeicherten Daten
@app.route("/pdf")
def pdf_export():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            content = f.read()
        html = render_template("download.html", content=content)
        pdf = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html), dest=pdf)
        if pisa_status.err:
            return "PDF-Fehler: konnte nicht erzeugt werden."
        pdf.seek(0)
        return send_file(pdf, mimetype="application/pdf", as_attachment=True, download_name="ausbildungsdaten.pdf")
    except Exception as e:
        return f"Fehler bei der PDF-Erzeugung: {e}"

# App starten
if __name__ == "__main__":
    app.run(debug=True)
