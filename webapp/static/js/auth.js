/* =============================================================
   MÓDULO DE AUTENTICACIÓN
   ============================================================= */

export async function procesarLogin() {
    console.log(">> Auth: Intentando Login...");
    const emailInput = document.getElementById('login-email');
    const passInput = document.getElementById('login-pass');

    if (!emailInput || !passInput) return;

    const datos = new URLSearchParams();
    datos.append('email', emailInput.value);
    datos.append('password', passInput.value);

    try {
        const respuesta = await fetch('/login', { method: 'POST', body: datos });
        const resultado = await respuesta.json();

        if (resultado.exito) {
            localStorage.setItem('usuario_logueado', resultado.nombre);
            alert(`¡Bienvenido, ${resultado.nombre}!`);
            window.location.href = 'index.html';
        } else {
            alert("Error: " + resultado.mensaje);
        }
    } catch (error) {
        console.error(error);
        alert("Error de conexión con el servidor.");
    }
}

export async function procesarRegistro() {
    console.log(">> Auth: Intentando Registro...");
    const nombreInput = document.getElementById('reg-nombre');
    const emailInput = document.getElementById('reg-email');
    const passInput = document.getElementById('reg-pass');

    if (!nombreInput || !emailInput || !passInput) return;

    const datos = new URLSearchParams();
    datos.append('nombre', nombreInput.value);
    datos.append('email', emailInput.value);
    datos.append('password', passInput.value);

    try {
        const respuesta = await fetch('/register', { method: 'POST', body: datos });
        const resultado = await respuesta.json();

        if (resultado.exito) {
            alert("¡Registro exitoso! Inicia sesión.");
            window.location.href = 'login.html';
        } else {
            alert("Hubo un problema con el registro.");
        }
    } catch (error) {
        console.error(error);
        alert("Error de conexión.");
    }
}

export function actualizarHeaderSesion() {
    const usuario = localStorage.getItem('usuario_logueado');
    const navInvitado = document.getElementById('nav-invitado');
    const navUsuario = document.getElementById('nav-usuario');
    const spanNombre = document.getElementById('header-nombre-usuario');

    if (usuario) {
        if (navInvitado) navInvitado.style.display = 'none';
        if (navUsuario) navUsuario.style.display = 'flex';
        if (spanNombre) spanNombre.textContent = usuario;
    } else {
        if (navInvitado) navInvitado.style.display = 'flex';
        if (navUsuario) navUsuario.style.display = 'none';
    }
}

export function cerrarSesion() {
    if (confirm("¿Cerrar sesión?")) {
        localStorage.removeItem('usuario_logueado');
        window.location.href = 'index.html';
    }
}