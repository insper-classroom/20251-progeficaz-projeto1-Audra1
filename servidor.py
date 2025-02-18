from flask import Flask, render_template, request, redirect, jsonify
import views
from database import init_db, get_db


app = Flask(__name__)

# Configurando a pasta de arquivos estáticos
app.static_folder = 'static'

# Initialize database when app starts
init_db()

# home 
@app.route('/')
@app.route('/<space_name>')
def index(space_name='default'):
    space_id = views.get_or_create_space(space_name)
    spaces = views.get_spaces()
    return render_template('index.html', 
                         notes=views.get_notes(space_id),
                         spaces=spaces,
                         current_space=space_name)


# submit 
@app.route('/submit', methods=['POST'])
def submit_form():
    space_id = request.form.get('space_id')
    titulo = request.form.get('titulo')
    detalhes = request.form.get('detalhes')
    
    views.submit(space_id, titulo, detalhes)
    return redirect(f'/{request.form.get("space")}')

@app.route('/update/<int:note_id>', methods=['POST'])
def update_note(note_id):
    data = request.get_json()
    with get_db() as db:
        db.execute(
            'UPDATE notes SET title = ?, details = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (data['title'], data['details'], note_id)
        )
    return jsonify({'status': 'success'})

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    views.delete_note(note_id)
    return redirect('/')

@app.route('/create-space', methods=['POST'])
def create_space():
    data = request.get_json()
    space_name = data.get('name')
    
    if not space_name:
        return jsonify({'error': 'Space name is required'}), 400
        
    try:
        views.get_or_create_space(space_name)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-space/<int:space_id>', methods=['POST'])
def delete_space(space_id):
    try:
        with get_db() as db:
            # First delete all notes in the space
            db.execute('DELETE FROM notes WHERE space_id = ?', (space_id,))
            # Then delete the space
            db.execute('DELETE FROM spaces WHERE id = ?', (space_id,))
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
