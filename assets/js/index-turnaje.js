function toggleTournament(element) {
    const content = element.nextElementSibling;
    const isActive = element.classList.contains('active');
    
    document.querySelectorAll('.tournament-header.active').forEach(header => {
        if (header !== element) {
            header.classList.remove('active');
            header.nextElementSibling.classList.remove('active');
        }
    });

    element.classList.toggle('active');
    content.classList.toggle('active');
    
    if (!isActive) {
        content.style.maxHeight = content.scrollHeight + "px";
    } else {
        content.style.maxHeight = null;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.tournament-content').forEach(content => {
        content.style.maxHeight = null;
    });
});
