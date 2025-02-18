from utils import load_data, load_template, save_data
import os
from database import get_db

def get_or_create_space(name):
    with get_db() as db:
        # Try to get existing space
        db.execute('SELECT id FROM spaces WHERE name = ?', (name,))
        space = db.fetchone()
        
        if space:
            return space[0]
            
        # Create new space if it doesn't exist
        db.execute('INSERT INTO spaces (name) VALUES (?)', (name,))
        return db.lastrowid

def get_spaces():
    with get_db() as db:
        db.execute('SELECT id, name FROM spaces ORDER BY name')
        return db.fetchall()

def get_notes(space_id):
    note_template = load_template('components/note/note.html')
    with get_db() as db:
        db.execute('''
            SELECT id, title, details 
            FROM notes 
            WHERE space_id = ?
            ORDER BY created_at DESC
        ''', (space_id,))
        notes = db.fetchall()
        notes_li = [
            note_template.format(
                id=f"{space_id}/{note[0]}",
                title=note[1], 
                details=note[2],
                details_class='visible' if note[2].strip() else ''
            ) for note in notes
        ]
    return '\n'.join(notes_li)

def index():
    return load_template('index.html')


def submit(space_id, title, details):
    with get_db() as db:
        db.execute('''
            INSERT INTO notes (space_id, title, details)
            VALUES (?, ?, ?)
        ''', (space_id, title, details))

def delete_note(note_id):
    with get_db() as db:
        db.execute('DELETE FROM notes WHERE id = ?', (note_id,))




