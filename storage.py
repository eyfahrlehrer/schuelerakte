# Schritt 4: Speichern der Daten in einer Datei (statt nur anzeigen)
# Diese neue Datei kannst du "storage.py" nennen und in dein Projektverzeichnis legen

def save_diagrammkarte(data):
    with open("saved_diagrammkarte.txt", "a", encoding="utf-8") as f:
        f.write("\n--- Neue Eintragung ---\n")
        for key, value in data.items():
            if isinstance(value, list):
                f.write(f"{key}: {', '.join(value)}\n")
            else:
                f.write(f"{key}: {value}\n")
