from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
import views
from database import init_db, get_db
import os


app = Flask(__name__)

# Configurando a pasta de arquivos estáticos
app.static_folder = 'static'

# Initialize database when app starts
init_db()

# Add this route before the space routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'visual', 'img'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

# home 
@app.route('/')
@app.route('/<space_name>')
def index(space_name='default'):
    if space_name == 'favicon.ico':
        return redirect('/')
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

@app.route('/delete/<path:note_id>', methods=['POST'])
def delete_note(note_id):
    # Split the composite ID into space_id and note_id
    space_id, actual_note_id = map(int, note_id.split('/'))
    views.delete_note(actual_note_id)
    return redirect(f'/{request.referrer.split("/")[-1]}')

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

@app.route('/update-space-name', methods=['POST'])
def update_space_name():
    data = request.get_json()
    space_id = data.get('space_id')
    new_name = data.get('name')
    
    try:
        with get_db() as db:
            db.execute('UPDATE spaces SET name = ? WHERE id = ?', (new_name, space_id))
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
