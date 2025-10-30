document.addEventListener('DOMContentLoaded', function() {
    const card = document.getElementById('logout-message');
    const countdownElement = document.getElementById('countdown');
    let countdown = 3;

    // 1. Activa la animación CSS (fade in/scale)
    // Esto hace que la tarjeta aparezca suavemente con el efecto 'show'
    setTimeout(() => {
        if (card) {
            card.classList.add('show');
        }
    }, 50);

    // 2. Controla la cuenta regresiva y la redirección
    if (countdownElement) {
        const intervalId = setInterval(function() {
            countdown -= 1;
            countdownElement.textContent = countdown;
            
            // 3. Redirige cuando el contador llega a cero
            if (countdown <= 0) {
                clearInterval(intervalId); // Detiene el contador
                // Usamos una redirección directa aquí, ya que no podemos usar {% url %} en archivos JS
                // Asumimos que la URL de login es '/login/'
                window.location.href = '/login/'; 
            }
        }, 1000); // 1 segundo
    }
});