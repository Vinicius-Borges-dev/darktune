const carousel = document.getElementById('image-carousel');
const items = carousel.querySelectorAll('.carousel-item');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
let currentIndex = 0;

function updateCarousel() {
  items.forEach((item, index) => {
    item.classList.remove('active', 'left', 'right');
    const relativeIndex = (index - currentIndex + items.length) % items.length;

    if (relativeIndex === 0) {
      item.classList.add('left'); // Imagem à esquerda
    } else if (relativeIndex === 1) {
      item.classList.add('active'); // Imagem central
    } else if (relativeIndex === 2) {
      item.classList.add('right'); // Imagem à direita
    }
  });
}

prevButton.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + items.length) % items.length;
  updateCarousel();
});

nextButton.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % items.length;
  updateCarousel();
});

// Inicializa o carrossel
updateCarousel();
