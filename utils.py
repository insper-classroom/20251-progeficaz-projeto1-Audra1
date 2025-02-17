import json 
import os


def load_data(filename):
    # definir caminho do arquivo
    filepath = os.path.join("static", "data", filename)

    # Abrindo e carregando JSON
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def load_template(filename):
    filepath = os.path.join("templates", filename)

    with open(filepath, "r", encoding = "utf-8") as file:
        conteudo = file.read()

    return conteudo
 

# salvar data que estou enviando no formulario no arquivo JSON.
def save_data(filename, data):
    filepath = os.path.join("static", "data", filename)
    with open(filepath, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # Como eu pego as info que eu digitei no momento que eu aperto "submit"

# ligar verde logo