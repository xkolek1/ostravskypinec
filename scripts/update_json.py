import json
import os
import re
import fitz # PyMuPDF
from datetime import datetime

# Cesty k souborům
PROPOZICE_DIR = 'assets/propozice'
ALBUMS_DIR = 'assets/images/albums'
JSON_FILE = 'data.json'

def extract_dates_from_pdf(pdf_path):
    """
    Otevře PDF, extrahuje text, odfiltruje nežádoucí řádky a najde všechna
    data ve formátech "dd. mm. yyyy" a "dd. <měsíc> yyyy".
    """
    dates = []
    
    # Slovník pro převod českých názvů měsíců (v 2. pádě) na čísla
    month_map = {
        'ledna': '01', 'února': '02', 'března': '03', 'dubna': '04',
        'května': '05', 'června': '06', 'července': '07', 'srpna': '08',
        'září': '09', 'října': '10', 'listopadu': '11', 'prosince': '12'
    }

    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        # Krok 1: Odstranění řádků, které nechceme prohledávat
        lines = full_text.splitlines()
        filtered_lines = [line for line in lines if not line.strip().lower().startswith("v ostravě dne")]
        filtered_text = "\n".join(filtered_lines)

        # Krok 2: Vylepšený regulární výraz
        # Hledá buď čísla (01-12) nebo názvy měsíců ze slovníku
        month_pattern = r'(\d{1,2}|' + '|'.join(month_map.keys()) + r')'
        date_pattern = r'\b(\d{1,2})\.\s*' + month_pattern + r'\s*\.\s*(\d{4})\b'

        found_matches = re.findall(date_pattern, filtered_text, re.IGNORECASE)

        # Krok 3: Zpracování a sjednocení formátu nalezených datumů
        for match in found_matches:
            day, month, year = match
            
            # Převedeme slovní měsíc na číslo, pokud je to potřeba
            if not month.isdigit():
                month = month_map[month.lower()]
            
            # Sestavíme finální formát a zajistíme dvouciferný formát pro den a měsíc
            formatted_date = f"{int(day):02d}. {int(month):02d}. {year}"
            
            if formatted_date not in dates:
                dates.append(formatted_date)

    except Exception as e:
        print(f"Chyba při zpracování PDF souboru {pdf_path}: {e}")
    
    # Seřadíme data pro lepší přehlednost
    return sorted(dates)


def update_json_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'tournaments': [], 'photo_albums': []}

    existing_tournaments = {t['fileName'] for t in data['tournaments']}
    existing_albums = {a['albumName'] for a in data['photo_albums']}
    
    today = datetime.now().strftime('%Y-%m-%d')

    # Zpracování propozic
    os.makedirs(PROPOZICE_DIR, exist_ok=True)
    for file_name in os.listdir(PROPOZICE_DIR):
        if file_name.endswith('.pdf') and file_name not in existing_tournaments:
            print(f"Nalezeny nové propozice: {file_name}")
            pdf_path = os.path.join(PROPOZICE_DIR, file_name)
            
            tournament_dates = extract_dates_from_pdf(pdf_path)
            print(f"Nalezená a zpracovaná data v souboru: {tournament_dates}")

            data['tournaments'].append({
                'fileName': file_name,
                'pushDate': today,
                'tournamentDates': tournament_dates
            })

    # Zpracování fotoalb (beze změny)
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

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    update_json_data()