/* =============================================================
   MÓDULO DE INTERFAZ DE USUARIO (UI)
   ============================================================= */

export function mostrarNotificacion(mensaje) {
    const toast = document.getElementById("toast-box");
    // Si no existe el elemento en el HTML, lo creamos al vuelo
    if (!toast && document.body) {
        const div = document.createElement("div");
        div.id = "toast-box";
        document.body.appendChild(div);
    }
    
    const toastElem = document.getElementById("toast-box");
    if (toastElem) {
        toastElem.textContent = `✅ ${mensaje}`;
        toastElem.className = "show";
        setTimeout(() => { 
            toastElem.className = toastElem.className.replace("show", ""); 
        }, 3000);
    }
}

export function iniciarSaludoDinamico() {
    const heroContent = document.querySelector('.hero-content');
    // Evitar duplicados
    if (heroContent && !document.getElementById('saludo-dinamico')) {
        const hora = new Date().getHours();
        let texto = "";
        if (hora < 12) texto = "¡Buenos días! Empieza con energía ☀️";
        else if (hora < 19) texto = "¡Buenas tardes! Hora del café ☕";
        else texto = "¡Buenas noches! Code & Chill 🌙";

        const p = document.createElement('p');
        p.id = 'saludo-dinamico';
        p.textContent = texto;
        p.style.color = "#f39c12"; 
        p.style.fontWeight = "bold";
        p.style.fontSize = "1.2rem";
        heroContent.prepend(p);
    }
}

export function iniciarFlipCards() {
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.classList.toggle('flipped');
        });
    });
}

export function iniciarLogoInteractivo() {
    const logos = document.querySelectorAll('.logo');
    logos.forEach(el => {
        // Hacerlo focusable para teclado si no lo es
        if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'button');
        el.setAttribute('aria-pressed', 'false');

        el.addEventListener('click', () => {
            el.classList.toggle('logo--active');
            const pressed = el.classList.contains('logo--active');
            el.setAttribute('aria-pressed', pressed ? 'true' : 'false');
        });

        el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                el.click();
            }
        });
    });
}