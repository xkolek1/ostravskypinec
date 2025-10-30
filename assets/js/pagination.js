document.addEventListener('DOMContentLoaded', () => {
    const bodyId = document.body.id;

    if (bodyId === 'page-turnaje' || bodyId === 'page-zpravodaje') {
        const dataType = (bodyId === 'page-turnaje') ? 'tournaments' : 'zpravodaje';
        initSeasonPaginator(dataType);
    } else if (bodyId === 'page-foto') {
        initPhotoPaginator();
    }
});

/**
 * =================================================================
 * PAGINÁTOR SEZÓN (pro Turnaje a Zpravodaje)
 * =================================================================
 */
async function initSeasonPaginator(dataType) {
    const container = document.getElementById('content-container');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    
    if (!container || !prevButton || !nextButton || !pageInfo) {
        console.error('Chybí potřebné HTML elementy pro paginátor sezón.');
        return;
    }

    let allSeasons = [];
    let allItems = [];
    let currentSeasonIndex = 0;

    try {
        const response = await fetch('data.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        // 1. Shromáždíme data podle typu stránky
        if (dataType === 'tournaments') {
            allItems = [
                ...(data.tournaments || []).map(item => ({ ...item, type: 'propozice' })),
                ...(data.results || []).map(item => ({ ...item, type: 'vysledky' }))
            ];
        } else { // 'zpravodaje'
            allItems = (data.zpravodaje || []).map(item => ({ ...item, type: 'zpravodaje' }));
        }

        if (allItems.length === 0) {
            container.innerHTML = '<p>Pro tuto sekci nebyla nalezena žádná data.</p>';
            pageInfo.textContent = 'Žádná data';
            prevButton.disabled = true;
            nextButton.disabled = true;
            return;
        }

        // 2. Získáme unikátní sezóny a seřadíme je sestupně (2025, 2024, ...)
        const seasonSet = new Set(allItems.map(item => item.season));
        allSeasons = Array.from(seasonSet).sort((a, b) => b.localeCompare(a));
        
        if (allSeasons.length === 0) {
             container.innerHTML = '<p>Nebyly nalezeny žádné sezóny.</p>';
             return;
        }

        // 3. Vytvoříme 'page' divy pro každou sezónu
        container.innerHTML = ''; // Vyčistíme "Načítám..."
        allSeasons.forEach((season, index) => {
            const pageDiv = document.createElement('div');
            pageDiv.className = 'page';
            pageDiv.dataset.season = season;
            if (index === 0) {
                pageDiv.classList.add('active'); // První je aktivní
            }
            container.appendChild(pageDiv);
        });

        // 4. Naplníme divy obsahem
        allItems.sort((a, b) => new Date(b.pushDate) - new Date(a.pushDate));
        
        allItems.forEach(item => {
            const seasonContainer = container.querySelector(`.page[data-season="${item.season}"]`);
            if (seasonContainer) {
                let itemHtml = '';
                if (item.type === 'propozice') {
                    itemHtml = `
                    <a class="tournament-header" href="assets/propozice/${item.season}/${item.originalFile}" target="_blank" rel="noopener">
                        <div class="tournament-name">P: ${item.fileName}</div>
                        <div class="tournament-date">${item.pushDate}</div>
                    </a>`;
                } else if (item.type === 'vysledky') {
                    itemHtml = `
                    <a class="tournament-header" href="assets/vysledky/${item.season}/${item.originalFile}" target="_blank" rel="noopener">
                        <div class="tournament-name">V: ${item.fileName}</div>
                        <div class="tournament-date">${item.pushDate}</div>
                    </a>`;
                } else if (item.type === 'zpravodaje') {
                     itemHtml = `
                    <a class="tournament-header" href="assets/zpravodaje/${item.season}/${item.originalFile}" target="_blank" rel="noopener">
                        <div class="tournament-name">${item.fileName}</div>
                        <div class="tournament-date">${item.pushDate}</div>
                    </a>`;
                }
                seasonContainer.innerHTML += itemHtml;
            }
        });

        // 5. Přidáme archivní odkazy na poslední (nejstarší) stránku
        const lastSeasonPage = container.querySelector(`.page[data-season="${allSeasons[allSeasons.length - 1]}"]`);
        if (lastSeasonPage) {
            if (dataType === 'tournaments') {
                lastSeasonPage.innerHTML += `
                    <hr style="margin: 20px 0;">
                    <a href="https://github.com/xkolek1/ostravskypinec/tree/main/assets/propozice" target="_blank" rel="noopener" class="tournament-header">
                        <div class="tournament-name">Archiv všech propozic</div>
                    </a>
                    <a href="https://github.com/xkolek1/ostravskypinec/tree/main/assets/vysledky" target="_blank" rel="noopener" class="tournament-header">
                        <div class="tournament-name">Archiv všech výsledků</div>
                    </a>
                `;
            } else if (dataType === 'zpravodaje') {
                lastSeasonPage.innerHTML += `
                    <hr style="margin: 20px 0;">
                    <a href="https://github.com/xkolek1/ostravskypinec/tree/main/assets/zpravodaje" target="_blank" rel="noopener" class="tournament-header">
                        <div class="tournament-name">Archiv všech zpravodajů</div>
                    </a>
                `;
            }
        }
        
        // 6. Inicializujeme paginátor
        updatePaginatorUI();

    } catch (error) {
        console.error('Chyba při načítání dat pro sezóny:', error);
        container.innerHTML = '<p>Nepodařilo se načíst data.</p>';
    }

    function updatePaginatorUI() {
        container.querySelectorAll('.page').forEach((page, index) => {
            page.classList.toggle('active', index === currentSeasonIndex);
        });

        const currentSeason = allSeasons[currentSeasonIndex];
        pageInfo.textContent = `Sezona ${currentSeason}/${parseInt(currentSeason) + 1}`;

        prevButton.disabled = currentSeasonIndex === 0;
        nextButton.disabled = currentSeasonIndex === allSeasons.length - 1;
    }

    prevButton.addEventListener('click', () => {
        if (currentSeasonIndex > 0) {
            currentSeasonIndex--;
            updatePaginatorUI();
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentSeasonIndex < allSeasons.length - 1) {
            currentSeasonIndex++;
            updatePaginatorUI();
        }
    });
}


/**
 * =================================================================
 * ČÍSELNÝ PAGINÁTOR (pro Foto)
 * =================================================================
 */
async function initPhotoPaginator() {
    const gridContainer = document.getElementById('album-grid-container');
    const paginationContainer = document.getElementById('pagination-container');
    const fotogalerieSection = document.getElementById('fotogalerie');
    
    if (!gridContainer || !paginationContainer || !fotogalerieSection) {
        console.error('Chybí potřebné HTML elementy pro paginátor fotek.');
        return;
    }

    let allAlbums = [];
    const albumsPerPage = 6; 
    
    // Zjistíme aktuální stránku z URL (např. foto.html?page=3)
    const initialUrlParams = new URLSearchParams(window.location.search);
    let currentPage = parseInt(initialUrlParams.get('page')) || 1;

    function scrollToGalleryTop() {
        fotogalerieSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Přidán druhý parametr 'updateHistory', abychom zabránili smyčce při volání z 'popstate'
    function renderPage(page, updateHistory = true) {
        currentPage = page;
        gridContainer.innerHTML = '';
        const start = (page - 1) * albumsPerPage;
        const end = start + albumsPerPage;
        const paginatedAlbums = allAlbums.slice(start, end);

        paginatedAlbums.forEach(album => {
            // Přidáme '&returnPage=${currentPage}' do odkazu na album
            const albumCardHtml = `
                <a href="album.html?album=${encodeURIComponent(album.albumName)}&returnPage=${currentPage}" class="album-card" title="${album.displayName}">
                    <div class="album-thumbnail" style="background-image: url('${album.previewImage}')"></div>
                    <div class="album-title">${album.displayName} <br> <small style="color: #6c757d;">${album.pushDate}</small></div>
                </a>
            `;
            gridContainer.innerHTML += albumCardHtml;
        });

        // Pokud je voláno kliknutím, aktualizujeme URL v prohlížeči
        if (updateHistory) {
            const url = new URL(window.location);
            url.searchParams.set('page', page);
            // pushState změní URL a přidá položku do historie prohlížeče
            history.pushState({page: page}, '', url);
        }

        updatePaginationButtons(); 
    }

    function setupPagination(pageCount) {
        paginationContainer.innerHTML = '';
        if (pageCount <= 1) return;

        const prevButton = document.createElement('button');
        prevButton.innerHTML = '&laquo;';
        prevButton.title = 'Předchozí';
        prevButton.className = 'pagination-prev';
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                renderPage(currentPage - 1); // Volání renderPage automaticky aktualizuje historii
                scrollToGalleryTop();
            }
        });
        paginationContainer.appendChild(prevButton);

        const pageNumbersContainer = document.createElement('div');
        pageNumbersContainer.className = 'page-numbers';
        paginationContainer.appendChild(pageNumbersContainer);

        const nextButton = document.createElement('button');
        nextButton.innerHTML = '&raquo;';
        nextButton.title = 'Další';
        nextButton.className = 'pagination-next';
        nextButton.addEventListener('click', () => {
            if (currentPage < pageCount) {
                renderPage(currentPage + 1); // Volání renderPage automaticky aktualizuje historii
                scrollToGalleryTop();
            }
        });
        paginationContainer.appendChild(nextButton);
        
        updatePaginationButtons();
    }

    function updatePaginationButtons() {
        const pageCount = Math.ceil(allAlbums.length / albumsPerPage);
        const prevButton = paginationContainer.querySelector('.pagination-prev');
        const nextButton = paginationContainer.querySelector('.pagination-next');
        const pageNumbersContainer = paginationContainer.querySelector('.page-numbers');
        
        if (prevButton) prevButton.disabled = currentPage === 1;
        if (nextButton) nextButton.disabled = currentPage === pageCount;

        renderPageNumbers(pageCount, pageNumbersContainer);
    }

    function renderPageNumbers(pageCount, container) {
        container.innerHTML = ''; 
        const siblingCount = 2; 

        const createPageButton = (page, isActive, textOverride) => {
            const button = document.createElement('button');
            button.innerText = textOverride || page; 
            button.className = 'page-number-btn';
            button.title = `Přejít na stránku ${page}`; 
            if (isActive) {
                button.classList.add('active');
            }
            button.addEventListener('click', () => {
                renderPage(page); // Volání renderPage automaticky aktualizuje historii
                scrollToGalleryTop();
            });
            container.appendChild(button);
        };

        const createEllipsis = () => {
            const ellipsis = document.createElement('span');
            ellipsis.innerText = '...';
            ellipsis.className = 'pagination-ellipsis';
            container.appendChild(ellipsis);
        };

        createPageButton(1, currentPage === 1); 

        const leftSibling = Math.max(2, currentPage - siblingCount);
        if (leftSibling > 2) {
            createEllipsis();
        }

        const rightSibling = Math.min(pageCount - 1, currentPage + siblingCount);
        for (let i = leftSibling; i <= rightSibling; i++) {
            createPageButton(i, currentPage === i);
        }

        if (rightSibling < pageCount - 1) {
            createEllipsis();
        }

        if (pageCount > 1) { 
            createPageButton(pageCount, currentPage === pageCount); 
        }
    }

    // --- Start načítání dat pro Foto ---
    try {
        const response = await fetch('data.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        
        if (!data.photo_albums || data.photo_albums.length === 0) {
            gridContainer.innerHTML = '<p>Momentálně zde nejsou žádná fotoalba.</p>';
            return;
        }
        
        allAlbums = data.photo_albums.sort((a, b) => new Date(b.pushDate) - new Date(a.pushDate));
        
        const totalPages = Math.ceil(allAlbums.length / albumsPerPage);
        
        setupPagination(totalPages); 
        
        // *** ZMĚNA č.3: První vykreslení ***
        // Poprvé vykreslíme stránku BEZ aktualizace historie (protože URL už je správné)
        renderPage(currentPage, false); 

        // *** ZMĚNA č.4: Listener pro tlačítko Zpět v prohlížeči ***
        window.addEventListener('popstate', (event) => {
            // Zjistíme, na jakou stránku se historie posunula
            const page = (event.state && event.state.page) 
                ? event.state.page 
                : (parseInt(new URLSearchParams(window.location.search).get('page')) || 1);
            
            // Vykreslíme danou stránku, ale už nevoláme pushState (historii změnil prohlížeč)
            renderPage(page, false);
        });
        
    } catch (error) {
        console.error('Chyba při načítání fotoalb:', error);
        gridContainer.innerHTML = '<p>Nepodařilo se načíst fotoalba.</p>';
    }
}