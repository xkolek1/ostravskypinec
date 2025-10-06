document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const totalPages = 3;
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    function updatePagination() {
        // Skrýt všechny stránky
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Zobrazit aktuální stránku
        document.getElementById(`page-${currentPage}`).classList.add('active');

        // Aktualizovat tlačítka
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;

        // Aktualizovat informace o stránce
        pageInfo.textContent = `Sezona ${Math.abs(currentPage - 2026)} / ${Math.abs(currentPage - 2027)}`;
    }

    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    nextButton.addEventListener('click', function () {
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    // Inicializace
    updatePagination();
});