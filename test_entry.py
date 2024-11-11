# test_entry.py
from app import app, db, Todo
from datetime import datetime, timezone

with app.app_context():
    # Erstelle einen Test-Eintrag
    try:
        new_todo = Todo(content="Flask-App entwickeln")
        db.session.add(new_todo)
        db.session.commit()
        print("Test-Eintrag erfolgreich erstellt!")
        
        # Überprüfe den Eintrag
        todos = Todo.query.all()
        print(f"\nAlle Einträge in der Datenbank:")
        for todo in todos:
            print(f"ID: {todo.id}, Aufgabe: {todo.content}, Erstellt: {todo.date_created}")
            
    except Exception as e:
        print(f"Fehler: {e}")