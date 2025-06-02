from sqlalchemy import Column, Integer, String, Boolean, Date
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
