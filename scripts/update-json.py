import json
import os
from datetime import datetime
import subprocess

# Cesty k souborům
PROPOZICE_DIR = 'assets/propozice'
ALBUMS_DIR = 'assets/images/albums'
JSON_FILE = 'data.json'

def get_added_files():
    """Získá seznam přidaných souborů v posledním commitu."""
    # Git příkaz pro získání seznamu změněných souborů
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def update_json_data():
    # Načtení stávajících dat z JSON souboru
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Pokud soubor neexistuje nebo je prázdný, vytvoříme novou strukturu
        data = {'tournaments': [], 'photo_albums': []}

    added_files = get_added_files()
    today = datetime.now().strftime('%Y-%m-%d')

    for file_path in added_files:
        # Zpracování PDF propozic
        if file_path.startswith(PROPOZICE_DIR) and file_path.endswith('.pdf'):
            file_name = os.path.basename(file_path)
            # Zkontrolujeme, zda již záznam neexistuje
            if not any(t['fileName'] == file_name for t in data['tournaments']):
                print(f"Nalezeny nové propozice: {file_name}")
                data['tournaments'].append({
                    'fileName': file_name,
                    'pushDate': today
                })

        # Zpracování fotoalb
        if file_path.startswith(ALBUMS_DIR):
            # Získáme název alba (název složky)
            album_name = file_path.split('/')[3]
            if not any(a['albumName'] == album_name for a in data['photo_albums']):
                # Najdeme první obrázek v albu jako náhled
                album_path = os.path.join(ALBUMS_DIR, album_name)
                try:
                    first_image = sorted([f for f in os.listdir(album_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])[0]
                    preview_image = os.path.join(album_path, first_image)
                    
                    print(f"Nalezeno nové fotoalbum: {album_name}")
                    data['photo_albums'].append({
                        'albumName': album_name,
                        'pushDate': today,
                        'previewImage': preview_image
                    })
                except IndexError:
                    print(f"Varování: V albu '{album_name}' nebyly nalezeny žádné obrázky.")


    # Uložení aktualizovaných dat zpět do JSON souboru
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    update_json_data()