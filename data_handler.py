import json
import os

def get_json_path():
    """Obtener la ruta del archivo JSON donde se guardan los datos."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'stadium_data.json')

def save_to_json(country, stadium_data):
    """Guardar datos en un archivo JSON."""
    data = load_from_json()
    if data is None:
        data = {}
    data[country] = stadium_data
    json_path = get_json_path()
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json():
    """Cargar datos desde un archivo JSON."""
    json_path = get_json_path()
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    else:
        return None
