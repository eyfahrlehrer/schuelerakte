from db import Base, engine
from models import Fahrschueler

# Tabelle erstellen (falls nicht vorhanden)
print("🚀 Starte Datenbanktabellen-Erstellung ...")
Base.metadata.create_all(bind=engine)
print("✅ Tabellen wurden erfolgreich erstellt!")
