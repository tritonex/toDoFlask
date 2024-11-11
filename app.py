from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os
print(os.getcwd())  # Zeigt das aktuelle Arbeitsverzeichnis

app = Flask(__name__)

# Absoluter Pfad zur Datenbank
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Datenbank-Pfad: {db_path}")  # Debug-Ausgabe

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_target = db.Column(db.DateTime, nullable=True)  # Zieldatum kann leer sein
    task_done = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Entfernt führende/nachfolgende Leerzeichen
        task_content = request.form['content'].strip()
        date_target_str = request.form.get('date_target', '')
        
        if not task_content:
            return 'Task content cannot be empty'
        
        new_task = Todo(content=task_content)
        
        # Setze das Zieldatum, wenn eines angegeben wurde
        if date_target_str:
            try:
                date_target = datetime.strptime(date_target_str, '%Y-%m-%d')
                new_task.date_target = date_target
            except ValueError:
                return 'Invalid date format', 400
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return 'Database error occurred', 500
    
    # Sortiere Tasks: Erst nicht erledigte Tasks nach Datum, dann erledigte Tasks nach Datum
    tasks = Todo.query.order_by(
        Todo.task_done.asc(),  # Nicht erledigte Tasks zuerst
        Todo.date_target.asc().nullslast(),  # Nach Datum sortieren, NULL-Werte am Ende
        Todo.date_created.desc()  # Bei gleichem Status und Datum: neuere Tasks zuerst
    ).all()
    
    return render_template('index.html', tasks=tasks)

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_status(id):
    task = Todo.query.get_or_404(id)
    task.task_done = not task.task_done
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return 'Problem updating task status', 500
    return redirect('/')
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        # Handle the date_target update
        date_target_str = request.form.get('date_target', '')
        if date_target_str:
            try:
                task.date_target = datetime.strptime(date_target_str, '%Y-%m-%d')
            except ValueError:
                return 'Invalid date format', 400
        else:
            task.date_target = None

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)