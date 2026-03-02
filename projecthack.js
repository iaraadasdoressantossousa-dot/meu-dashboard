let currentSlide = 1;

// Iniciar o slider
startSlider();

// Função para iniciar o slider
function startSlider() {
    setInterval(function () {
        nextSlide();
    }, 5000); // Altere o valor 2000 para ajustar o intervalo em milissegundos (3 segundos neste caso)
}

// Função para ir para a próxima imagem
function nextSlide() {
    currentSlide++;

    if (currentSlide > 4) {
        currentSlide = 1;
    }

    showSlide(currentSlide);
}

// Função para exibir uma imagem específica
function showSlide(index) {
    // Desmarcar todas as rádio-buttons
    for (let i = 1; i <= 4; i++) {
        document.getElementById("radio" + i).checked = false;
    }

    // Marcar a rádio-button correspondente à imagem atual
    document.getElementById("radio" + index).checked = true;
}