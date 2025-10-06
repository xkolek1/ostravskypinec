function toggleTournament(element) {
    const content = element.nextElementSibling;
    const isActive = element.classList.contains('active');
    
    // Zavřít všechny ostatní otevřené turnaje
    document.querySelectorAll('.tournament-header.active').forEach(header => {
        if (header !== element) {
            header.classList.remove('active');
            header.nextElementSibling.classList.remove('active');
        }
    });
    
    // Přepnout aktuální turnaj
    element.classList.toggle('active');
    content.classList.toggle('active');
    
    // Pokud se otevírá, nastavit max-height podle obsahu
    if (!isActive) {
        content.style.maxHeight = content.scrollHeight + "px";
    } else {
        content.style.maxHeight = null;
    }
}

// Uzavření všech turnajů při načtení stránky
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.tournament-content').forEach(content => {
        content.style.maxHeight = null;
    });
});
