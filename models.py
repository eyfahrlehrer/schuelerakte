from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fahrschueler(Base):
    __tablename__ = "fahrschueler"  # So heißt die Tabelle in der Datenbank

    id = Column(Integer, primary_key=True)
    name = Column(String)
    vorname = Column(String)
    geburtsdatum = Column(Date)
    adresse = Column(String)
    mobil = Column(String)
    sehhilfe = Column(Boolean)
    theorie_bestanden = Column(Boolean)
