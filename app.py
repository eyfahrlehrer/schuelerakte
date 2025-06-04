from flask import Flask, render_template, request, redirect, url_for, session, send_file
import io
from xhtml2pdf import pisa
from storage import save_diagrammkarte
from flask import render_template
from db import SessionLocal
from models import Schueler
from models import Ueberlandfahrt

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

@app.route("/neuer_schueler")
def neuer_schueler():
    return redirect(url_for("stammdaten"))


@app.route("/stammdaten", methods=["GET", "POST"])
def stammdaten():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            name = request.form.get("name")
            vorname = request.form.get("vorname")
            geburtsdatum = request.form.get("geburtsdatum")
            strasse = request.form.get("strasse")
            hausnummer = request.form.get("hausnummer")
            plz = request.form.get("plz")
            ort = request.form.get("ort")
            mobil = request.form.get("mobil")
            sehhilfe = "sehhilfe" in request.form
            theorie_bestanden = "theorie_bestanden" in request.form

            neuer_schueler = Fahrschueler(
                name=name,
                vorname=vorname,
                geburtsdatum=geburtsdatum,
                strasse=strasse,
                hausnummer=hausnummer,
                plz=plz,
                ort=ort,
                mobil=mobil,
                sehhilfe=sehhilfe,
                theorie_bestanden=theorie_bestanden
            )

            db = SessionLocal()
            db.add(neuer_schueler)
            db.commit()
            db.refresh(neuer_schueler)

            session["stammdaten"] = {
                "id": neuer_schueler.id,
                "name": name,
                "vorname": vorname,
                "geburtsdatum": geburtsdatum
            }

            return redirect(url_for("grundstufe"))
        
        except Exception as e:
            flash(f"Fehler beim Speichern: {e}", "danger")
        
        finally:
            db.close()

    return render_template("stammdaten.html")

@app.route("/alle_schueler", methods=["GET"])
def alle_schueler():
    db = SessionLocal()
    schueler_liste = db.query(Fahrschueler).all()
    db.close()
    return render_template("alle_schueler.html", schueler=schueler_liste)

@app.route("/grundstufe", methods=["GET", "POST"])
def grundstufe():
    if "username" not in session:
        return redirect(url_for("login"))

    status = ""
    schueler_id = session.get("stammdaten", {}).get("id")

    if not schueler_id:
        status = "❌ Fehler: Stammdaten nicht vorhanden!"
        return render_template("grundstufe.html", status=status)

    if request.method == "POST":
        eintrag = Grundstufe(
            schueler_id=schueler_id,
            sitz="sitz" in request.form,
            spiegel="spiegel" in request.form,
            lenkrad="lenkrad" in request.form,
            kopfstuetze="kopfstuetze" in request.form,
            einweisung="einweisung" in request.form,
            pedale="pedale" in request.form,
            gang="gang" in request.form,
            sicht="sicht" in request.form,
            schaltuebung=request.form.get("schaltuebung", ""),
            notizen=request.form.get("notizen", "")
        )

        db = SessionLocal()
        db.add(eintrag)
        db.commit()
        db.close()

        status = "✅ Grundstufe gespeichert!"

    return render_template("grundstufe.html", status=status)

@app.route("/aufbaustufe", methods=["GET", "POST"])
def aufbaustufe():
    if "username" not in session:
        return redirect(url_for("login"))

    status = ""
    schueler_id = session.get("stammdaten", {}).get("id")

    if not schueler_id:
        status = "❌ Fehler: Stammdaten nicht vorhanden!"
        return render_template("aufbaustufe.html", status=status)

    if request.method == "POST":
        daten = Aufbaustufe(
            schueler_id=schueler_id,
            rollen_schalten="rollen_schalten" in request.form,
            bremsen_schalten="bremsen_schalten" in request.form,
            bremsuebung_degressiv="bremsuebung_degressiv" in request.form,
            bremsuebung_ziel="bremsuebung_ziel" in request.form,
            bremsuebung_gefahr="bremsuebung_gefahr" in request.form,
            gefaelle_anfahren="gefaelle_anfahren" in request.form,
            gefaelle_rueckwaerts="gefaelle_rueckwaerts" in request.form,
            gefaelle_schalten="gefaelle_schalten" in request.form,
            steigungen_anfahren="steigungen_anfahren" in request.form,
            steigungen_anfahren_rueck="steigungen_anfahren_rueck" in request.form,
            steigungen_sichern="steigungen_sichern" in request.form,
            steigungen_schalten="steigungen_schalten" in request.form,
            tastgeschwindigkeit="tastgeschwindigkeit" in request.form,
            bedienung_kontrolleinr="bedienung_kontrolleinr" in request.form,
            besondere_oertliche="besondere_oertliche" in request.form,
            notizen=request.form.get("notizen", "")
        )

        db = SessionLocal()
        db.add(daten)
        db.commit()
        db.close()

        status = "✅ Aufbaustufe gespeichert!"

    return render_template("aufbaustufe.html", status=status)


@app.route("/leistungsstufe", methods=["GET", "POST"])
def leistungsstufe():
    if request.method == "POST":
        # Hier später Verarbeitung der Formulardaten möglich
        print("Leistungsstufe wurde abgeschickt:", request.form)
    return render_template("leistungsstufe.html")

@app.route("/aufbaustufe", methods=["GET", "POST"])
def aufbaustufe_formular():
    if "username" not in session:
        return redirect(url_for("login"))

    status = ""
    schueler_id = session.get("stammdaten", {}).get("id")

    if not schueler_id:
        status = "❌ Fehler: Stammdaten nicht vorhanden!"
        return render_template("aufbaustufe.html", status=status)

    if request.method == "POST":
        daten = Aufbaustufe(
            schueler_id=schueler_id,
            rollen_schalten=bool(request.form.get("rollen_schalten")),
            bremsen_schalten=bool(request.form.get("bremsen_schalten")),

            bremsuebung_degressiv=bool(request.form.get("bremsuebung_degressiv")),
            bremsuebung_ziel=bool(request.form.get("bremsuebung_ziel")),
            bremsuebung_gefahr=bool(request.form.get("bremsuebung_gefahr")),

            gefaelle_anfahren=bool(request.form.get("gefaelle_anfahren")),
            gefaelle_anhalten=bool(request.form.get("gefaelle_anhalten")),
            gefaelle_rueckwaerts=bool(request.form.get("gefaelle_rueckwaerts")),
            gefaelle_sichern=bool(request.form.get("gefaelle_sichern")),
            gefaelle_schalten=bool(request.form.get("gefaelle_schalten")),

            steigungen_anfahren=bool(request.form.get("steigungen_anfahren")),
            steigungen_anhalten=bool(request.form.get("steigungen_anhalten")),
            steigungen_rueckwaerts=bool(request.form.get("steigungen_rueckwaerts")),
            steigungen_sichern=bool(request.form.get("steigungen_sichern")),
            steigungen_schalten=bool(request.form.get("steigungen_schalten")),

            tastgeschwindigkeit=bool(request.form.get("tastgeschwindigkeit")),
            bedienung_kontrolle=bool(request.form.get("bedienung_kontrolle")),
            besondere_oertliche=bool(request.form.get("besondere_oertliche")),

            notizen=request.form.get("notizen", "")
        )

        db = SessionLocal()
        db.add(daten)
        db.commit()
        db.close()

        status = "✅ Aufbaustufe gespeichert!"

    return render_template("aufbaustufe.html", status=status)

@app.route("/grundfahraufgaben", methods=["GET", "POST"])
def grundfahraufgaben():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = Grundfahraufgaben(
            schueler_id=session.get("schueler_id"),
            rueckwaerts_ecke=bool(request.form.get("rueckwaerts_ecke")),
            einparken_laengs_rueck=bool(request.form.get("einparken_laengs_rueck")),
            einparken_quer_rueck=bool(request.form.get("einparken_quer_rueck")),
            einparken_links_vor=bool(request.form.get("einparken_links_vor")),
            einparken_rechts_vor=bool(request.form.get("einparken_rechts_vor")),
            umkehren=bool(request.form.get("umkehren")),
            gefahrenbremsung=bool(request.form.get("gefahrenbremsung")),
            notizen=request.form.get("notizen")
        )
        db.session.add(eintrag)
        db.session.commit()
        return render_template("grundfahraufgaben.html", status="✅ Grundfahraufgaben gespeichert")

    return render_template("grundfahraufgaben.html")


@app.route("/ueberlandfahrt", methods=["GET", "POST"])
def ueberlandfahrt():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = {
            "stammdaten": session.get("stammdaten", {}),
            "ueberlandfahrt": {
                "angepasste_geschwindigkeit": "angepasste_geschwindigkeit" in request.form,
                "abstand_vorne": "abstand_vorne" in request.form,
                "abstand_hinten": "abstand_hinten" in request.form,
                "abstand_seitlich": "abstand_seitlich" in request.form,
                "beobachtungsspiegel": "beobachtungsspiegel" in request.form,
                "verkehrszeichen": "verkehrszeichen" in request.form,
                "kreuzungen_einmuendungen": "kreuzungen_einmuendungen" in request.form,
                "kurven": "kurven" in request.form,
                "steigerung": "steigerung" in request.form,
                "gefaelle": "gefaelle" in request.form,
                "alleen": "alleen" in request.form,
                "ueberholen": "ueberholen" in request.form,
                "liegen_geblieben": "liegen_geblieben" in request.form,
                "fussgaenger": "fussgaenger" in request.form,
                "ortseinfahrt": "ortseinfahrt" in request.form,
                "wildtiere": "wildtiere" in request.form,
                "leistungsgrenze": "leistungsgrenze" in request.form,
                "ablenkung": "ablenkung" in request.form,
                "orientierung": "orientierung" in request.form,
                "notizen": request.form.get("notizen")
            }
        }

        # In Datei speichern
        os.makedirs("db", exist_ok=True)
        with open("db/saved_ueberlandfahrt.txt", "a", encoding="utf-8") as f:
            f.write(str(eintrag) + "\n")

        return render_template("ueberlandfahrt.html", status="✅ Überlandfahrt gespeichert")

    return render_template("ueberlandfahrt.html")
    

@app.route("/autobahnfahrt", methods=["GET", "POST"])
def autobahnfahrt():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = {
            "stammdaten": session.get("stammdaten", {}),
            "autobahnfahrt": {
                "fahrtplanung": "fahrtplanung" in request.form,
                "einfahrt_bab": "einfahrt_bab" in request.form,
                "freistreifenwahl": "freistreifenwahl" in request.form,
                "geschwindigkeit": "geschwindigkeit" in request.form,
                "abstand_vorne": "abstand_vorne" in request.form,
                "abstand_hinten": "abstand_hinten" in request.form,
                "abstand_seitlich": "abstand_seitlich" in request.form,
                "ueberholen": "ueberholen" in request.form,
                "schilder_markierung": "schilder_markierung" in request.form,
                "vorbeifahren_anschlussstellen": "vorbeifahren_anschlussstellen" in request.form,
                "rast_tankstellen": "rast_tankstellen" in request.form,
                "verhalten_unfall": "verhalten_unfall" in request.form,
                "dichter_verkehr": "dichter_verkehr" in request.form,
                "besondere_situation": "besondere_situation" in request.form,
                "leistungsgrenze": "leistungsgrenze" in request.form,
                "ablenkung": "ablenkung" in request.form,
                "konfliktsituation": "konfliktsituation" in request.form,
                "verlassen_bab": "verlassen_bab" in request.form,
                "notizen": request.form.get("notizen")
            }
        }
        return render_template("autobahnfahrt.html", status="✅ Autobahnfahrt gespeichert", **eintrag)

    return render_template("autobahnfahrt.html")
    

@app.route("/daemmerung", methods=["GET", "POST"])
def daemmerung():
    if "username" not in session:
        return redirect(url_for("login"))

    status = ""
    schueler_id = session.get("stammdaten", {}).get("id")

    if not schueler_id:
        status = "❌ Fehler: Stammdaten nicht vorhanden!"
        return render_template("daemmerung.html", status=status)

    if request.method == "POST":
        eintrag = Daemmerung(
            schueler_id=schueler_id,
            beleuchtung="beleuchtung" in request.form,
            kontrolle="kontrolle" in request.form,
            benutzung="benutzung" in request.form,
            einstellen="einstellen" in request.form,
            fernlicht="fernlicht" in request.form,
            beleuchtete_strasse="beleuchtete_strasse" in request.form,
            unbeleuchtete_strasse="unbeleuchtete_strasse" in request.form,
            parken="parken" in request.form,

            besondere_situationen="besondere_situationen" in request.form,
            schlechte_witterung="schlechte_witterung" in request.form,
            bahnuebergaenge="bahnuebergaenge" in request.form,
            tiere="tiere" in request.form,
            unbeleuchtete_verkehrsteilnehmer="unbeleuchtete_verkehrsteilnehmer" in request.form,
            besondere_anforderungen="besondere_anforderungen" in request.form,
            blendung="blendung" in request.form,
            orientierung="orientierung" in request.form,
            abschlussbesprechung="abschlussbesprechung" in request.form,

            notizen=request.form.get("notizen", "")
        )

        db = SessionLocal()
        db.add(eintrag)
        db.commit()
        db.close()

        status = "✅ Dämmerungsfahrt gespeichert!"
        return render_template("daemmerung.html", status=status)

    return render_template("daemmerung.html")


# Route: Gespeicherte Daten anzeigen
@app.route("/anzeigen")
def anzeigen():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            daten = f.readlines()
    except FileNotFoundError:
        return render_template("anzeigen.html", fehler="Noch keine Einträge vorhanden.")

    return render_template("anzeigen.html", eintraege=daten)
    

@app.route("/reifestufe", methods=["GET", "POST"])
def reifestufe():
    if "username" not in session:
        return redirect(url_for("login"))

    status = ""
    schueler_id = session.get("stammdaten", {}).get("id")

    if not schueler_id:
        status = "❌ Fehler: Stammdaten nicht vorhanden!"
        return render_template("reifestufe.html", status=status)

    if request.method == "POST":
        eintrag = Reifestufe(
            schueler_id=schueler_id,
            selbststaendiges_fahren=bool(request.form.get("selbststaendiges_fahren")),
            innerorts=bool(request.form.get("innerorts")),
            ausserorts=bool(request.form.get("ausserorts")),
            verantwortungsbewusstes_fahren=bool(request.form.get("verantwortungsbewusstes_fahren")),
            testfahrt=bool(request.form.get("testfahrt")),
            fakts=bool(request.form.get("fakts")),
            andere=bool(request.form.get("andere")),
            wiederholung_vertiefung=bool(request.form.get("wiederholung_vertiefung")),
            leistungsbewertung=bool(request.form.get("leistungsbewertung")),
            notizen=request.form.get("notizen", "")
        )

        db.session.add(eintrag)
        db.session.commit()

        status = "✅ Reifestufe gespeichert ✅"
        return render_template("reifestufe.html", status=status)

    return render_template("reifestufe.html")
    

@app.route("/technik", methods=["GET", "POST"])
def technik():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        eintrag = {
            "stammdaten": session.get("stammdaten", {}),
            "technik": dict(request.form)
        }

        return render_template("technik.html", status="✅ Technik gespeichert")

    return render_template("technik.html")

@app.route("/profil")
def profil():
    if "username" not in session:
        return redirect(url_for("login"))

    db = SessionLocal()
    schueler = db.query(Fahrschueler).first()  # Später mit Filter: .filter_by(name=session["name"]).first()
    db.close()

    return render_template("profil.html", schueler=schueler)

# Route: PDF-Export der gespeicherten Daten
@app.route("/pdf")
def pdf_export():
    try:
        with open("saved_diagrammkarte.txt", "r", encoding="utf-8") as f:
            content = f.readlines()

        html = render_template("download.html", content=content)
        pdf = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html), dest=pdf)
        if pisa_status.err:
            return "PDF-Fehler: konnte nicht erzeugt werden."
        pdf.seek(0)
        return send_file(pdf, mimetype="application/pdf", as_attachment=True, download_name="ausbildungsdaten.pdf")
    except Exception as e:
        return f"Fehler bei der PDF-Erzeugung: {e}"
