def get_all_students():
    return [
        {"id": 1, "name": "Max Mustermann", "progress": "Grundstoff abgeschlossen"},
        {"id": 2, "name": "Lisa Beispiel", "progress": "Sonderfahrten in Planung"},
    ]

def add_student(name, progress):
    # Das wird später erweitert
    pass

students = [
    {"id": 1, "name": "Max Mustermann", "progress": "Grundstoff abgeschlossen"},
    {"id": 2, "name": "Lisa Beispiel", "progress": "Sonderfahrten in Planung"},
]

def get_all_students():
    return students

def add_student(name, progress):
    new_id = max(s["id"] for s in students) + 1 if students else 1
    students.append({"id": new_id, "name": name, "progress": progress})
