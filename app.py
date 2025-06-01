from flask import Flask, render_template, request, redirect, url_for, session, send_file
import io
from xhtml2pdf import pisa

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

# Route: Formular zur Diagrammkarte
@app.route("/diagrammkarte", methods=["GET", "POST"])
def diagrammkarte():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form.get("name", "")
        daten = dict(request.form)
        daten.pop("name", None)  # „Name“-Feld separat
        with open("saved_diagrammkarte.txt", "w", encoding="utf-8") as f:
            f.write(f"Name: {name}\n")
            for feld, wert in daten.items():
                f.write(f"{feld}: {wert}\n")
        return redirect(url_for("anzeigen"))
    return render_template("diagrammkarte.html")

# Route: Anzeige gespeicherter Daten
@app.route("/saved")
def anzeigen():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            daten = f.read()
        return render_template("anzeigen.html", daten=daten)
    except FileNotFoundError:
        return render_template("anzeigen.html", fehler="❌ Noch keine Daten gespeichert.")

# Route: PDF-Download
@app.route("/download/pdf")
def download_pdf():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            content = f.read()

        html = f"""
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
        <h1>Gespeicherte Ausbildungsdaten</h1>
        <pre>{content}</pre>
        </body>
        </html>
        """

        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html), dest=result)
        result.seek(0)

        if pisa_status.err:
            return "PDF konnte nicht erstellt werden.", 500

        return send_file(result, mimetype='application/pdf', as_attachment=True, download_name='ausbildungsdaten.pdf')

    except FileNotFoundError:
        return render_template("anzeigen.html", fehler="❌ Es gibt noch keine gespeicherten Daten zum PDF-Download.")

@app.route("/anzeigen")
def anzeigen():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            eintraege = f.read().split("---\n")
    except FileNotFoundError:
        eintraege = []

    return render_template("anzeigen.html", eintraege=eintraege)


# Server starten
if __name__ == "__main__":
    app.run(debug=True)
