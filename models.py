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
