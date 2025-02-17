from utils import load_data
from database import get_db, init_db

def migrate_json_to_sqlite():
    # Initialize the database first
    init_db()
    
    # Load JSON data
    try:
        notes = load_data('notes.json')
    except FileNotFoundError:
        print("No JSON file found to migrate")
        return

    # Insert into SQLite
    with get_db() as db:
        for note in notes:
            db.execute(
                'INSERT INTO notes (title, details) VALUES (?, ?)',
                (note.get('titulo', ''), note.get('detalhes', ''))
            )
        print("Migration completed successfully")

if __name__ == "__main__":
    migrate_json_to_sqlite()
