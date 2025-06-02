import os
from sqlalchemy import create_engine
from models import Base

# Erstelle Engine aus Umgebungsvariable
engine = create_engine(os.getenv("postgresql://postgres:REfUKSgpPmQQiVgXupXEKLhHcourNHIr@mainline.proxy.rlwy.net:55720/railway"))

print("🚀 Starte Datenbanktabellen-Erstellung ...")
Base.metadata.create_all(engine)
print("✅ Tabellen erfolgreich erstellt.")
