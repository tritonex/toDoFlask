# create_db.py
from app import app, db, Todo  # Todo hier importieren
import os
from sqlalchemy import inspect

print(f"Aktuelles Verzeichnis: {os.getcwd()}")
print(f"Datenbank-URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    print("Erstelle Datenbank neu...")
    db.drop_all()  # Löscht die alte Datenbank
    db.create_all()
    print("Datenbank wurde neu erstellt!")
    
    # Prüfen, ob die Tabelle existiert
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Vorhandene Tabellen: {tables}")

    # Teste die Verbindung
    try:
        todos = db.session.query(Todo).all()
        print("Datenbankabfrage erfolgreich!")
        print(f"Anzahl Einträge: {len(todos)}")
    except Exception as e:
        print(f"Fehler bei der Datenbankabfrage: {e}")