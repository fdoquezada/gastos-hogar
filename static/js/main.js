// Versión con efectos más pronunciados
document.addEventListener('DOMContentLoaded', function() {
    // Efecto "levitar" más pronunciado para tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.transition = 'all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.2)';
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15)';
            this.style.zIndex = '1';
        });
    });
    
    // Animación de entrada más dramática
    const statCards = document.querySelectorAll('.card.border-left-primary, .card.border-left-success, .card.border-left-info, .card.border-left-danger');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px) rotateX(10deg)';
        card.style.transformOrigin = 'center bottom';
        
        setTimeout(() => {
            card.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) rotateX(0)';
        }, index * 200);
    });

    // Efecto para botones con "rebote" sutil
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.style.transition = 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.05)';
            this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
        
        // Efecto al hacer clic
        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(-1px) scale(0.98)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-4px) scale(1.05)';
        });
    });
});

// Efectos para el formulario de login
document.addEventListener('DOMContentLoaded', function() {
    const loginCard = document.querySelector('.login-card');
    const inputs = document.querySelectorAll('.login-card input');
    
    // Efecto de entrada para la tarjeta
    if (loginCard) {
        loginCard.style.opacity = '0';
        loginCard.style.transform = 'scale(0.9) translateY(30px)';
        
        setTimeout(() => {
            loginCard.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            loginCard.style.opacity = '1';
            loginCard.style.transform = 'scale(1) translateY(0)';
        }, 300);
    }
    
    // Efectos para los inputs
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
});