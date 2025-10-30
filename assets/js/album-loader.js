document.addEventListener('DOMContentLoaded', () => {

    const gridContainer = document.getElementById('photo-grid-container');
    const albumTitle = document.getElementById('album-title');

    // Načteme VŠECHNY parametry z URL
    const urlParams = new URLSearchParams(window.location.search);
    const albumName = urlParams.get('album');
    const returnPage = urlParams.get('returnPage') || 1; // Získáme stránku, kam se vrátit

    // Aktualizujeme všechny odkazy "Zpět" na stránce
    const backLinks = document.querySelectorAll('.back-link');
    backLinks.forEach(link => {
        link.href = `foto.html?page=${returnPage}`;
    });

    if (!albumName) {
        albumTitle.textContent = 'Album nenalezeno';
        gridContainer.innerHTML = '<p>Chyba: V URL adrese chybí identifikátor alba.</p>';
        return;
    }

    // 2. Načteme data.json
    fetch('data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // 3. Najdeme správný objekt alba
            const album = data.photo_albums.find(a => a.albumName === albumName);

            if (!album) {
                albumTitle.textContent = 'Album nenalezeno';
                gridContainer.innerHTML = `<p>Chyba: Album s názvem "${albumName}" nebylo v datech nalezeno.</p>`;
                return;
            }

            // 4. Nastavíme titulek stránky a název sekce
            albumTitle.textContent = album.displayName;
            document.title = `${album.displayName} - MěSST Ostrava`;

            // 5. Zkontrolujeme, zda album obsahuje fotky
            if (!album.photos || album.photos.length === 0) {
                gridContainer.innerHTML = '<p>Toto album zatím neobsahuje žádné fotografie.</p>';
                return;
            }

            // --- Dynamická detekce cesty PRO TOTO ALBUM ---
            
            let baseUrl = '';
            const cloudflarePrefix = 'https://pub-32012a38b98242498823abfd03e3d82b.r2.dev';

            // Podíváme se na 'previewImage' tohoto konkrétního alba
            if (album.previewImage && album.previewImage.startsWith(cloudflarePrefix)) {
                // Pokud je náhled z Cloudflare, celé album je na Cloudflare
                baseUrl = `${cloudflarePrefix}/foto/`;
                console.log(`Album '${album.albumName}': Detekována Cloudflare cesta.`);
            } else {
                // Jinak předpokládáme lokální cestu (např. 'assets/foto/...')
                baseUrl = 'assets/foto/';
                console.log(`Album '${album.albumName}': Detekována lokální cesta.`);
            }


            // 6. Vygenerujeme HTML pro každou fotku
            let htmlToInject = '';
            album.photos.forEach(photoName => {
                // Sestavíme finální URL k fotce (pomocí námi určené baseUrl)
                const photoUrl = `${baseUrl}${encodeURIComponent(album.albumName)}/${encodeURIComponent(photoName)}`;
                
                htmlToInject += `
                    <a href="${photoUrl}" target="_blank" rel="noopener" class="photo-item" title="Zobrazit plnou velikost">
                        <img src="${photoUrl}" alt="${album.displayName} - ${photoName}" loading="lazy">
                    </a>
                `;
            });

            // 7. Vložíme všechny fotky najednou do kontejneru
            gridContainer.innerHTML = htmlToInject;

        })
        .catch(error => {
            console.error('Chyba při načítání dat alba:', error);
            albumTitle.textContent = 'Chyba načítání';
            gridContainer.innerHTML = '<p>Nepodařilo se načíst data alba. Zkuste to prosím později.</p>';
        });
});