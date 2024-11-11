# Flask Todo App

A simple todo application built with Flask.

## Features

- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Set due dates for tasks
- Mobile-responsive design
- Sort tasks by completion status

## Installation

1. Clone the repository

```bash
git clone https://github.com/IHR_USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install flask flask-sqlalchemy
```

4. Initialize the database

```bash
python create_db.py
```

5. Run the application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
flask-todo-app/
├── app.py              # Main application file
├── create_db.py        # Database initialization
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Main todo list
│   └── update.html    # Update task form
└── test.db            # SQLite database
```

## Technologies Used

- Flask
- SQLAlchemy
- HTML/CSS
- SQLite

## License

This project is licensed under the MIT License - see the LICENSE file for details.
Last edited vor 8 Minuten
