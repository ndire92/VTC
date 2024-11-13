// JavaScript pour le Slider
let currentIndex = 0;

function showNextSlide() {
    const slider = document.querySelector('.slider');
    const totalSlides = document.querySelectorAll('.slide').length;

    // Mettre à jour l'index
    currentIndex = (currentIndex + 1) % totalSlides;

    // Changer la position du slider
    slider.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Changer de slide toutes les 3 secondes
setInterval(showNextSlide, 3000);
