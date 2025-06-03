from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Schueler(Base):
    __tablename__ = "schueler"

    id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False)
    geburtsdatum = Column(Date, nullable=True)
    adresse = Column(String, nullable=True)
    mobilnummer = Column(String, nullable=True)
    sehhilfe = Column(Boolean, default=False)
    theorie_bestanden = Column(Boolean, default=False)
    grundfahraufgaben = relationship("Grundfahraufgaben", back_populates="schueler", uselist=False)
    ueberlandfahrt = relationship("Ueberlandfahrt", back_populates="schueler", uselist=False)
    daemmerung = relationship("Daemmerung", back_populates="schueler", uselist=False)
    reifestufe = relationship("Reifestufe", back_populates="schueler", uselist=False)
    technik = relationship("Technik", uselist=False, back_populates="schueler")


    
class Grundstufe(Base):
    __tablename__ = "grundstufe"

    id = Column(Integer, primary_key=True, index=True)
    schueler_id = Column(Integer, nullable=False)

    sitz = Column(Boolean, default=False)
    spiegel = Column(Boolean, default=False)
    lenkrad = Column(Boolean, default=False)
    kopfstuetze = Column(Boolean, default=False)
    einweisung = Column(Boolean, default=False)
    pedale = Column(Boolean, default=False)
    gang = Column(Boolean, default=False)
    sicht = Column(Boolean, default=False)

    schaltuebung = Column(String, nullable=True)
    notizen = Column(String, nullable=True)

class Aufbaustufe(Base):
    __tablename__ = "aufbaustufe"

    id = Column(Integer, primary_key=True, index=True)
    schueler_id = Column(Integer, nullable=False)

    rollen_schalten = Column(Boolean, default=False)
    bremsen_schalten = Column(Boolean, default=False)

    bremsuebung_degressiv = Column(Boolean, default=False)
    bremsuebung_ziel = Column(Boolean, default=False)
    bremsuebung_gefahr = Column(Boolean, default=False)

    gefaelle_anfahren = Column(Boolean, default=False)
    gefaelle_anhalten = Column(Boolean, default=False)
    gefaelle_rueckwaerts = Column(Boolean, default=False)
    gefaelle_sichern = Column(Boolean, default=False)
    gefaelle_schalten = Column(Boolean, default=False)

    steigungen_anfahren = Column(Boolean, default=False)
    steigungen_anhalten = Column(Boolean, default=False)
    steigungen_rueckwaerts = Column(Boolean, default=False)
    steigungen_sichern = Column(Boolean, default=False)
    steigungen_schalten = Column(Boolean, default=False)

    tastgeschwindigkeit = Column(Boolean, default=False)
    bedienung_kontrolle = Column(Boolean, default=False)
    besondere_oertliche = Column(Boolean, default=False)

    notizen = Column(String, nullable=True)
    

class Grundfahraufgaben(Base):
    __tablename__ = "grundfahraufgaben"

    id = Column(Integer, primary_key=True)
    schueler_id = Column(Integer, ForeignKey("schueler.id"), nullable=False)

    rueckwaerts_ecke = Column(Boolean, default=False)
    einparken_laengs_rueck = Column(Boolean, default=False)
    einparken_quer_rueck = Column(Boolean, default=False)
    einparken_links_vor = Column(Boolean, default=False)
    einparken_rechts_vor = Column(Boolean, default=False)
    umkehren = Column(Boolean, default=False)
    gefahrenbremsung = Column(Boolean, default=False)
    notizen = Column(String)

    schueler = relationship("Schueler", back_populates="grundfahraufgaben")
    

class Ueberlandfahrt(Base):
    __tablename__ = "ueberlandfahrt"

    id = Column(Integer, primary_key=True)
    schueler_id = Column(Integer, ForeignKey("schueler.id"), nullable=False)

    geschwindigkeit = Column(Boolean, default=False)
    abstand_vorne = Column(Boolean, default=False)
    abstand_hinten = Column(Boolean, default=False)
    abstand_seitlich = Column(Boolean, default=False)

    beobachtung = Column(Boolean, default=False)
    schilder = Column(Boolean, default=False)
    kurven = Column(Boolean, default=False)
    einmuendungen = Column(Boolean, default=False)

    besonderheiten = Column(Boolean, default=False)
    fussgaenger = Column(Boolean, default=False)
    einfahren_ortschaft = Column(Boolean, default=False)
    wildtiere = Column(Boolean, default=False)

    leistungsgrenze = Column(Boolean, default=False)
    ablenkung = Column(Boolean, default=False)
    orientierung = Column(Boolean, default=False)

    notizen = Column(String)

    schueler = relationship("Schueler", back_populates="ueberlandfahrt")
    

class Daemmerung(Base):
    __tablename__ = "daemmerung"

    id = Column(Integer, primary_key=True)
    schueler_id = Column(Integer, ForeignKey("schueler.id"), nullable=False)

    beleuchtung = Column(Boolean, default=False)
    kontrolle = Column(Boolean, default=False)
    benutzung = Column(Boolean, default=False)
    einstellen = Column(Boolean, default=False)
    fernlicht = Column(Boolean, default=False)
    beleuchtete_strasse = Column(Boolean, default=False)
    unbeleuchtete_strasse = Column(Boolean, default=False)
    parken = Column(Boolean, default=False)

    besondere_situationen = Column(Boolean, default=False)
    schlechte_witterung = Column(Boolean, default=False)
    bahnuebergaenge = Column(Boolean, default=False)
    tiere = Column(Boolean, default=False)
    unbeleuchtete_verkehrsteilnehmer = Column(Boolean, default=False)
    besondere_anforderungen = Column(Boolean, default=False)
    blendung = Column(Boolean, default=False)
    orientierung = Column(Boolean, default=False)
    abschlussbesprechung = Column(Boolean, default=False)

    notizen = Column(String)

    schueler = relationship("Schueler", back_populates="daemmerung")
    

class Reifestufe(Base):
    __tablename__ = "reifestufe"

    id = Column(Integer, primary_key=True)
    schueler_id = Column(Integer, ForeignKey("schueler.id"), nullable=False)

    selbststaendiges_fahren = Column(Boolean, default=False)
    innerorts = Column(Boolean, default=False)
    ausserorts = Column(Boolean, default=False)
    verantwortungsbewusstes_fahren = Column(Boolean, default=False)
    testfahrt = Column(Boolean, default=False)
    fakts = Column(Boolean, default=False)
    andere = Column(Boolean, default=False)
    wiederholung_vertiefung = Column(Boolean, default=False)
    leistungsbewertung = Column(Boolean, default=False)
    notizen = Column(String)

    schueler = relationship("Schueler", back_populates="reifestufe")

class Technik(Base):
    __tablename__ = "technik"

    id = Column(Integer, primary_key=True)
    schueler_id = Column(Integer, ForeignKey("schueler.id"), nullable=False)

    # Reifen
    reifen_beschaedigung = Column(Boolean, default=False)
    profiltiefe_druck = Column(Boolean, default=False)

    # Lichtanlage
    standlicht = Column(Boolean, default=False)
    abbendlicht = Column(Boolean, default=False)
    fernlicht = Column(Boolean, default=False)
    schlussleuchten = Column(Boolean, default=False)
    nebellicht = Column(Boolean, default=False)
    warnblinker = Column(Boolean, default=False)
    blinker = Column(Boolean, default=False)
    hupe = Column(Boolean, default=False)
    bremsleuchte = Column(Boolean, default=False)
    kontrollleuchten = Column(Boolean, default=False)

    # Lenkung
    lenkschloss = Column(Boolean, default=False)
    lenkspiel = Column(Boolean, default=False)

    # Bremsen
    betriebsbremse = Column(Boolean, default=False)
    feststellbremse = Column(Boolean, default=False)

    # Motorraum
    motoroel = Column(Boolean, default=False)
    kuehlmittel = Column(Boolean, default=False)
    wischwasser = Column(Boolean, default=False)

    # Tanken
    tanken = Column(Boolean, default=False)

    # Sicherungsmittel
    warndreieck = Column(Boolean, default=False)
    verbandskasten = Column(Boolean, default=False)
    bordwerkzeug = Column(Boolean, default=False)
    abschalten = Column(Boolean, default=False)

    # Außenkontrolle
    schaden_sauberkeit = Column(Boolean, default=False)
    scheibenwischer = Column(Boolean, default=False)
    kennzeichen = Column(Boolean, default=False)
    spiegel = Column(Boolean, default=False)
    beleuchtung = Column(Boolean, default=False)

    # Ladung
    ladung_sicherung = Column(Boolean, default=False)
    ladung_kennzeichnung = Column(Boolean, default=False)

    # Fahrerassistenzsysteme
    assistent_ein = Column(Boolean, default=False)
    assistent_anwenden = Column(Boolean, default=False)

    # Heizung / Lüftung
    heizung = Column(Boolean, default=False)
    lueftung = Column(Boolean, default=False)
    klimaanlage = Column(Boolean, default=False)
    heckscheibenheizung = Column(Boolean, default=False)
    sonderheizung = Column(Boolean, default=False)

    # Energiesparende Nutzung
    verbraucher_aus = Column(Boolean, default=False)
    abschalten_rechtzeitig = Column(Boolean, default=False)

    # Witterung
    schlechte_witterung = Column(Boolean, default=False)
    wit_lueftung = Column(Boolean, default=False)
    wit_beleuchtung = Column(Boolean, default=False)
    wit_scheibenwischer = Column(Boolean, default=False)
    regen = Column(Boolean, default=False)
    aquaplaning = Column(Boolean, default=False)
    wind = Column(Boolean, default=False)
    schnee_matsch = Column(Boolean, default=False)
    eis = Column(Boolean, default=False)

    # Notizen
    notizen = Column(String)

    # Beziehung zu Schüler
    schueler = relationship("Schueler", back_populates="technik")
