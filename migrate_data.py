from utils import load_data
from database import get_db, init_db

def migrate_json_to_sqlite():
    # Initialize the database first
    init_db()
    
    # Create default space
    with get_db() as db:
        db.execute('INSERT OR IGNORE INTO spaces (name) VALUES (?)', ('default',))
        db.execute('SELECT id FROM spaces WHERE name = ?', ('default',))
        default_space_id = db.fetchone()[0]
    
    # Load JSON data
    try:
        notes = load_data('notes.json')
    except FileNotFoundError:
        print("No JSON file found to migrate")
        return

    # Insert into SQLite with space_id
    with get_db() as db:
        for note in notes:
            db.execute(
                'INSERT INTO notes (space_id, title, details) VALUES (?, ?, ?)',
                (default_space_id, note.get('titulo', ''), note.get('detalhes', ''))
            )
        print("Migration completed successfully")

if __name__ == "__main__":
    migrate_json_to_sqlite()
