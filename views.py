from utils import load_data, load_template, save_data
import os

def get_notes():
    note_template = load_template('components/note/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    return '\n'.join(notes_li)

def index():
    return load_template('index.html')


def submit(titulo, detalhes):
    # Create the note dictionary with the actual variables (not string literals)
    note = {
        "titulo": titulo,
        "detalhes": detalhes
    }

    # Load existing notes
    notes = load_data('notes.json')
    
    # Append the new note
    notes.append(note)
    
    # Save the updated notes
    save_data('notes.json', notes)

    return




