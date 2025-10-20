import json
import os
from datetime import datetime

# Cesty k souborům
PROPOZICE_DIR = 'assets/propozice'
ALBUMS_DIR = 'assets/images/albums'
JSON_FILE = 'data.json'

def update_json_data():
    # Krok 1: Načtení stávajících dat z JSON souboru
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Pokud soubor neexistuje nebo je prázdný, vytvoříme novou strukturu
        data = {'tournaments': [], 'photo_albums': []}

    # Krok 2: Vytvoření seznamů již existujících položek pro snadné porovnání
    existing_tournaments = {t['fileName'] for t in data['tournaments']}
    existing_albums = {a['albumName'] for a in data['photo_albums']}
    
    today = datetime.now().strftime('%Y-%m-%d')

    # Krok 3: Zpracování propozic turnajů
    # Vytvoříme složku, pokud neexistuje, aby skript nespadl
    os.makedirs(PROPOZICE_DIR, exist_ok=True) 
    # Projdeme všechny soubory, které reálně existují ve složce
    for file_name in os.listdir(PROPOZICE_DIR):
        # Pokud soubor končí na .pdf a ještě není v našem JSONu, přidáme ho
        if file_name.endswith('.pdf') and file_name not in existing_tournaments:
            print(f"Nalezeny nové propozice: {file_name}")
            data['tournaments'].append({
                'fileName': file_name,
                'pushDate': today
            })

    # Krok 4: Zpracování fotoalb
    os.makedirs(ALBUMS_DIR, exist_ok=True)
    # Projdeme všechny podsložky (alba), které reálně existují
    for album_name in os.listdir(ALBUMS_DIR):
        album_path = os.path.join(ALBUMS_DIR, album_name)
        # Pokud se jedná o složku a ještě není v našem JSONu, přidáme ji
        if os.path.isdir(album_path) and album_name not in existing_albums:
            try:
                # Najdeme první obrázek v albu jako náhled
                images = sorted([f for f in os.listdir(album_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                if not images:
                    raise IndexError # Přeskočíme na 'except', pokud je složka prázdná
                
                preview_image_path = os.path.join(album_path, images[0])
                
                print(f"Nalezeno nové fotoalbum: {album_name}")
                data['photo_albums'].append({
                    'albumName': album_name,
                    'pushDate': today,
                    'previewImage': preview_image_path
                })
            except IndexError:
                print(f"Varování: Ve složce alba '{album_name}' nebyly nalezeny žádné obrázky.")

    # Krok 5: Uložení aktualizovaných dat zpět do JSON souboru
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    update_json_data()