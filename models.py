from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fahrschueler(Base):
    __tablename__ = "fahrschueler"  # Name der Tabelle in der Datenbank

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vorname = Column(String)
    geburtsdatum = Column(String)  # Oder Date, wenn du die Umwandlung in app.py sicherstellst
    strasse = Column(String)
    hausnummer = Column(String)
    mobil = Column(String)
    sehhilfe = Column(Boolean)
    theorie_bestanden = Column(Boolean)
