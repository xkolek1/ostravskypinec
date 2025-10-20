import json
import os
import re # Knihovna pro regulární výrazy (hledání vzorů v textu)
import fitz # Toto je knihovna PyMuPDF
from datetime import datetime

# Cesty k souborum
PROPOZICE_DIR = 'assets/propozice'
ALBUMS_DIR = 'assets/images/albums'
JSON_FILE = 'data.json'

def extract_dates_from_pdf(pdf_path):
    """Otevře PDF, extrahuje text a najde všechna data ve formátu dd. mm. yyyy."""
    dates = []
    try:
        # Otevření PDF souboru
        doc = fitz.open(pdf_path)
        full_text = ""
        # Projdeme každou stránku a spojíme text dohromady
        for page in doc:
            full_text += page.get_text()
        
        # Regulární výraz pro hledání data ve formátu dd. mm. yyyy (s tečkami i mezerami)
        # Najde např. "28. 09. 2025" nebo "22.11.2025"
        date_pattern = r'\b\d{1,2}\.\s*\d{1,2}\.\s*\d{4}\b'
        
        # Najdeme všechny odpovídající vzory
        found_dates = re.findall(date_pattern, full_text)
        
        # Očistíme formát (nahradíme různé mezery za jednotné) a odstraníme duplicity
        for date_str in found_dates:
            # Sjednotíme formát na "dd. mm. yyyy"
            cleaned_date = re.sub(r'\s+', ' ', date_str).strip()
            if cleaned_date not in dates:
                dates.append(cleaned_date)

    except Exception as e:
        print(f"Chyba při zpracování PDF souboru {pdf_path}: {e}")
    
    return dates

def update_json_data():
    # Krok 1: Načtení stávajících dat
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'tournaments': [], 'photo_albums': []}

    existing_tournaments = {t['fileName'] for t in data['tournaments']}
    existing_albums = {a['albumName'] for a in data['photo_albums']}
    
    today = datetime.now().strftime('%Y-%m-%d')

    # Krok 2: Zpracování propozic s extrakcí datumů
    os.makedirs(PROPOZICE_DIR, exist_ok=True) 
    for file_name in os.listdir(PROPOZICE_DIR):
        if file_name.endswith('.pdf') and file_name not in existing_tournaments:
            print(f"Nalezeny nové propozice: {file_name}")
            
            # Cesta k novému PDF souboru
            pdf_path = os.path.join(PROPOZICE_DIR, file_name)
            
            # Zavoláme novou funkci pro extrakci datumů
            tournament_dates = extract_dates_from_pdf(pdf_path)
            print(f"Nalezená data v souboru: {tournament_dates}")

            data['tournaments'].append({
                'fileName': file_name,
                'pushDate': today,
                'tournamentDates': tournament_dates # Přidáme pole s nalezenými datumy
            })

    # Krok 3: Zpracování fotoalb (zůstává stejné)
    os.makedirs(ALBUMS_DIR, exist_ok=True)
    for album_name in os.listdir(ALBUMS_DIR):
        album_path = os.path.join(ALBUMS_DIR, album_name)
        if os.path.isdir(album_path) and album_name not in existing_albums:
            try:
                images = sorted([f for f in os.listdir(album_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                if not images:
                    raise IndexError
                
                preview_image_path = os.path.join(album_path, images[0])
                
                print(f"Nalezeno nové fotoalbum: {album_name}")
                data['photo_albums'].append({
                    'albumName': album_name,
                    'pushDate': today,
                    'previewImage': preview_image_path
                })
            except IndexError:
                print(f"Varování: Ve složce alba '{album_name}' nebyly nalezeny žádné obrázky.")

    # Krok 4: Uložení dat
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    update_json_data()