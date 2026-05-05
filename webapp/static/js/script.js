
   //SCRIPT PRINCIPAL (CONTROLADOR DE MÓDULOS)

// 1. Importamos las funciones desde los otros archivos
import * as UI from './ui.js';
import * as Auth from './auth.js';
import * as Cart from './cart.js';

console.log("Cargando módulos JS...");

// 2. funcion para botones
window.procesarLogin = Auth.procesarLogin;
window.procesarRegistro = Auth.procesarRegistro;
window.cerrarSesion = Auth.cerrarSesion;
window.agregarAlCarrito = Cart.agregarAlCarrito;
window.finalizarCompra = Cart.finalizarCompra;
window.vaciarCarrito = Cart.vaciarCarrito;

// 3. inicio de pagina
document.addEventListener("DOMContentLoaded", () => {
    // Restaurar sesión y contadores
    Auth.actualizarHeaderSesion();
    Cart.actualizarContadorVisual();

    Cart.cargarTablaCarrito();

    UI.iniciarSaludoDinamico();
    UI.iniciarFlipCards();
    UI.iniciarLogoInteractivo();
});