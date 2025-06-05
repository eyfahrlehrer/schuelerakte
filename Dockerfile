# Verwende ein offizielles Python-Image
FROM python:3.12-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere Projektdateien in das Image
COPY . .

# Installiere Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Setze Umgebungsvariable für Flask (optional)
ENV FLASK_APP=app.py

# Starte die App
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
