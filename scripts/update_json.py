import json
import os
import re
import fitz # PyMuPDF
from datetime import datetime
import locale # Pro správné řazení českých datumů

# Nastavení českého locale pro správné řazení měsíců
try:
    locale.setlocale(locale.LC_TIME, 'cs_CZ.UTF-8')
except locale.Error:
    print("České locale 'cs_CZ.UTF-8' není dostupné. Řazení pravěpodobně nebude správné!")


# Cesty k souborům
PROPOZICE_DIR = 'assets/propozice'
VYSLEDKY_DIR = 'assets/vysledky'
ALBUMS_DIR = 'assets/images/albums' 
ZPRAVODAJE_DIR = 'assets/zpravodaje'
ZEBRICKY_D_DIR = 'assets/zebricky/dospeli'
ZEBRICKY_M_DIR = 'assets/zebricky/mladez'
JSON_FILE = 'data.json'

# Seznam souborů, které chceme ignorovat
IGNORE_FILES = {'.DS_Store', 'desktop.ini', 'Thumbs.db'}

def extract_dates_from_pdf(pdf_path):
    """
    Otevře PDF, extrahuje text, odfiltruje nežádoucí řádky a najde všechna
    data ve formátech "dd. mm. yyyy" a "dd. <měsíc> yyyy".
    """
    dates = []
    
    month_map = {
        'ledna': '01', 'února': '02', 'března': '03', 'dubna': '04',
        'května': '05', 'června': '06', 'července': '07', 'srpna': '08',
        'záři': '09', 'října': '10', 'listopadu': '11', 'prosince': '12',

        'leden': '01', 'únor': '02', 'březen': '03', 'duben': '04',
        'květen': '05', 'červen': '06', 'červenec': '07', 'srpen': '08',
        'září': '09', 'říjen': '10', 'listopad': '11', 'prosinec': '12'
    }

    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        lines = full_text.splitlines()
        filtered_lines = [line for line in lines if not line.strip().lower().startswith("v ostravě dne")]
        filtered_text = "\n".join(filtered_lines)

        month_pattern_keys = '|'.join(month_map.keys())
        date_pattern = re.compile(
            r'\b(\d{1,2})\.\s*(\d{1,2}|' + month_pattern_keys + r')\.?\s*(\d{4})\b',
            re.IGNORECASE
        )
        
        found_matches = date_pattern.findall(filtered_text)

        for match in found_matches:
            day, month, year = match
            
            month_str = str(month).lower()
            if not month_str.isdigit():
                month_num = month_map.get(month_str)
            else:
                month_num = month_str
            
            if month_num:
                formatted_date = f"{int(day):02d}. {int(month_num):02d}. {year}"
                if formatted_date not in dates:
                    dates.append(formatted_date)

    except Exception as e:
        print(f"Chyba při zpracování PDF souboru {pdf_path}: {e}")
    
    dates.sort(key=lambda date: datetime.strptime(date, "%d. %m. %Y"))
    return dates


def update_json_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'tournaments': [], 'results':[], 'photo_albums': [], 'zpravodaje': [], 'zebricky_dospeli': [], 'zebricky_mladez': []}

    existing_tournaments = {t['fileName'] for t in data['tournaments']}
    existing_results = {r['fileName'] for r in data['results']}
    existing_albums = {a['albumName'] for a in data['photo_albums']}
    existing_zpravodaje = {z['fileName'] for z in data.get('zpravodaje', [])}
    existing_zebricky_dospeli = {z['fileName'] for z in data.get('zebricky_dospeli', [])}
    existing_zebricky_mladez = {z['fileName'] for z in data.get('zebricky_mladez', [])}
    
    today = datetime.now().strftime('%Y-%m-%d')

    # --- ZPRACOVÁNÍ PROPOZIC ---
    os.makedirs(PROPOZICE_DIR, exist_ok=True)
    for season_folder in os.listdir(PROPOZICE_DIR):
        season_path = os.path.join(PROPOZICE_DIR, season_folder)
        if os.path.isdir(season_path):
            for file_name in os.listdir(season_path):
                base_name, extension = os.path.splitext(file_name)
                
                if extension == '.pdf' and base_name not in existing_tournaments:
                    print(f"Nalezeny nové propozice: {file_name} ve složce {season_folder}")
                    pdf_path = os.path.join(season_path, file_name)
                    
                    tournament_dates = extract_dates_from_pdf(pdf_path)
                    print(f"Nalezená a zpracovaná data v souboru: {tournament_dates}")

                    data['tournaments'].append({
                        'fileName': base_name,
                        'pushDate': today,
                        'tournamentDates': tournament_dates,
                        'originalFile': file_name,
                        'season': season_folder
                    })

    # --- ZPRACOVÁNÍ VÝSLEDKŮ ---
    os.makedirs(VYSLEDKY_DIR, exist_ok=True)
    for season_folder in os.listdir(VYSLEDKY_DIR):
        season_path = os.path.join(VYSLEDKY_DIR, season_folder)
        if os.path.isdir(season_path):
            for file_name in os.listdir(season_path):
                base_name, extension = os.path.splitext(file_name)

                if extension == '.pdf' and base_name not in existing_results:
                    print(f"Nalezeny nové výsledky: {file_name} ve složce {season_folder}")
                    pdf_path = os.path.join(season_path, file_name)

                    data['results'].append({
                        'fileName': base_name,
                        'pushDate': today,
                        'originalFile': file_name,
                        'season': season_folder
                    })

    # --- ZPRACOVÁNÍ ZPRAVODAJŮ ---
    os.makedirs(ZPRAVODAJE_DIR, exist_ok=True)
    for season_folder in os.listdir(ZPRAVODAJE_DIR):
        season_path = os.path.join(ZPRAVODAJE_DIR, season_folder)
        if os.path.isdir(season_path):
            for file_name in os.listdir(season_path):
                base_name, extension = os.path.splitext(file_name)

                if extension == '.pdf' and base_name not in existing_zpravodaje:
                    print(f"Nalezeny nové výsledky: {file_name} ve složce {season_folder}")
                    pdf_path = os.path.join(season_path, file_name)

                    data['zpravodaje'].append({
                        'fileName': base_name,
                        'pushDate': today,
                        'originalFile': file_name,
                        'season': season_folder
                    })
    
    # --- ZPRACOVÁNÍ ŽEBŘÍČKŮ DOSPĚLÝCH ---
    os.makedirs(ZEBRICKY_D_DIR, exist_ok=True)
    for file_name in os.listdir(ZEBRICKY_D_DIR):
        base_name, extension = os.path.splitext(file_name)

        if extension == '.pdf' and base_name not in existing_zebricky_dospeli:
            print(f"Nalezen žebříček dospělých: {file_name}")
            data['zebricky_dospeli'].append({
                'fileName': base_name,
                'pushDate': today,
                'originalFile': file_name
            })

    # --- ZPRACOVÁNÍ ŽEBŘÍČKŮ MLÁDEŽE ---
    os.makedirs(ZEBRICKY_M_DIR, exist_ok=True)
    for file_name in os.listdir(ZEBRICKY_M_DIR):
        base_name, extension = os.path.splitext(file_name)

        if extension == '.pdf' and base_name not in existing_zebricky_mladez:
            print(f"Nalezen žebříček mládeže: {file_name}")
            data['zebricky_mladez'].append({
                'fileName': base_name,
                'pushDate': today,
                'originalFile': file_name
            })

    # --- ZPRACOVÁNÍ NOVÝCH FOTOALB ---
    os.makedirs(ALBUMS_DIR, exist_ok=True)

    def strip_album_prefix(name):
        # odstraní prefix ve tvaru "123_"
        return re.sub(r'^\d{3}_', '', name)

    for album_name in os.listdir(ALBUMS_DIR):
        album_path = os.path.join(ALBUMS_DIR, album_name)
        
        # Zpracuje pouze pokud je to složka A ZÁROVEŇ ještě není v JSONu
        if os.path.isdir(album_path) and album_name not in existing_albums:
            
            # Najde všechny soubory, odfiltruje systémové a seřadí je
            images = sorted([
                f for f in os.listdir(album_path) 
                if f not in IGNORE_FILES and \
                   os.path.isfile(os.path.join(album_path, f))
            ])
            
            if not images:
                print(f"Varování: Ve složce alba '{album_name}' nebyly nalezeny žádné obrázky. Přeskakuji.")
                continue

            # Použije první obrázek jako náhled
            preview_image_filename = images[0]
            
            # preview_image_path = f"https://pub-32012a38b98242498823abfd03e3d82b.r2.dev/foto/{album_name}/{preview_image_filename}"
            preview_image_path = f"assets/images/albums/{album_name}/{preview_image_filename}"

            display_name = strip_album_prefix(album_name)

            print(f"Nalezeno nové fotoalbum: {album_name} (obsahuje {len(images)} fotek)")
            
            data['photo_albums'].append({
                'displayName': display_name,
                'albumName': album_name,
                'pushDate': today,
                'previewImage': preview_image_path,
                'photos': images
            })

    # --- ULOŽENÍ ZPĚT DO JSON ---
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"\nSoubor '{JSON_FILE}' byl úspěšně aktualizován.")

if __name__ == '__main__':
    update_json_data()