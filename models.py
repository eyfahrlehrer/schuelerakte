from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fahrschueler(Base):
    __tablename__ = "fahrschueler"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    vorname = Column(String, nullable=False)
    geburtsdatum = Column(String, nullable=False)  # Oder Date, wenn du mit Datumsformat arbeitest
    strasse = Column(String)
    hausnummer = Column(String)
    mobil = Column(String)
    sehhilfe = Column(Boolean, default=False)
    theorie_bestanden = Column(Boolean, default=False)

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

