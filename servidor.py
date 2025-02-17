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
def index():
    return render_template('index.html', notes=views.get_notes())


# submit 
@app.route('/submit', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo')  # Obtém o valor do campo 'titulo'
    detalhes = request.form.get('detalhes')  # Obtém o valor do campo 'detalhes'

    views.submit(titulo, detalhes)
    return redirect('/')

@app.route('/update/<int:note_id>', methods=['POST'])
def update_note(note_id):
    data = request.get_json()
    with get_db() as db:
        db.execute(
            'UPDATE notes SET title = ?, details = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (data['title'], data['details'], note_id)
        )
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
