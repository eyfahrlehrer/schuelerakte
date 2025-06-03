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
