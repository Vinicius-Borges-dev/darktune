window.onload = function () {
    const mensagens = document.querySelector('.notificacao');
    if (mensagens) {
        const tempoDeExibicao = 5000;
        setTimeout(function () {
            mensagens.style.display = 'none';
        }, tempoDeExibicao);
    }
};