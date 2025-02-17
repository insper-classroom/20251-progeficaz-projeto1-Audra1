from utils import load_data, load_template, save_data
import os
from database import get_db

def get_notes():
    note_template = load_template('components/note/note.html')
    with get_db() as db:
        db.execute('SELECT id, title, details FROM notes ORDER BY created_at DESC')
        notes = db.fetchall()
        notes_li = [
            note_template.format(
                id=note[0],
                title=note[1], 
                details=note[2],
                details_display='none' if not note[2].strip() else 'block'
            ) for note in notes
        ]
    return '\n'.join(notes_li)

def index():
    return load_template('index.html')


def submit(titulo, detalhes):
    with get_db() as db:
        db.execute(
            'INSERT INTO notes (title, details) VALUES (?, ?)',
            (titulo, detalhes)
        )

def delete_note(note_id):
    with get_db() as db:
        db.execute('DELETE FROM notes WHERE id = ?', (note_id,))




