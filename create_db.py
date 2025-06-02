import os
from sqlalchemy import create_engine
from models import Base

# Holt die Datenbank-URL aus der Railway-Umgebungsvariable
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("📡 Starte Datenbanktabellen-Erstellung ...")
Base.metadata.create_all(engine)
print("✅ Tabellen erfolgreich erstellt.")
