/* =============================================================
   MÓDULO DE CARRITO Y PEDIDOS
   ============================================================= */
import { mostrarNotificacion } from './ui.js';

export function agregarAlCarrito(nombre, precio) {
    let carrito = JSON.parse(localStorage.getItem('mi_carrito_cafe')) || [];
    carrito.push({ nombre: nombre, precio: precio });
    localStorage.setItem('mi_carrito_cafe', JSON.stringify(carrito));
    
    actualizarContadorVisual();
    mostrarNotificacion(`¡${nombre} agregado!`);
}

export function actualizarContadorVisual() {
    const carrito = JSON.parse(localStorage.getItem('mi_carrito_cafe')) || [];
    const contadorHeader = document.getElementById('contador-carrito');
    
    if (contadorHeader) contadorHeader.textContent = carrito.length;
}

export function cargarTablaCarrito() {
    const tabla = document.getElementById('cart-body');
    const totalSpan = document.getElementById('cart-total');
    
    if (!tabla) return; // No estamos en carrito.html

    let carrito = JSON.parse(localStorage.getItem('mi_carrito_cafe')) || [];
    let total = 0;
    tabla.innerHTML = ""; 

    if (carrito.length === 0) {
        tabla.innerHTML = "<tr><td colspan='2' style='text-align:center; padding:20px;'>Carrito vacío 🛒</td></tr>";
    } else {
        carrito.forEach((producto) => {
            let fila = `<tr><td>${producto.nombre}</td><td>$${parseFloat(producto.precio).toFixed(2)}</td></tr>`;
            tabla.innerHTML += fila;
            total += parseFloat(producto.precio);
        });
    }

    if (totalSpan) totalSpan.textContent = total.toFixed(2);
}

export function vaciarCarrito() {
    if (confirm("¿Vaciar carrito?")) {
        localStorage.removeItem('mi_carrito_cafe');
        location.reload();
    }
}

export function finalizarCompra() {
    let carrito = JSON.parse(localStorage.getItem('mi_carrito_cafe')) || [];

    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    let cliente = localStorage.getItem('usuario_logueado');
    if (!cliente) {
        let confirmar = confirm("No has iniciado sesión.\n\nAceptar: Ir a Login.\nCancelar: Modo Invitado.");
        if (confirmar) {
            window.location.href = "login.html";
            return;
        } else {
            cliente = prompt("Nombre para el pedido:");
        }
    }

    if (!cliente) return;

    let total = carrito.reduce((sum, item) => sum + item.precio, 0);
    
    let pedido = {
        cliente: cliente,
        productos: carrito,
        total: total
    };

    fetch('/api/pedido', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pedido)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            alert(`✅ ¡Gracias ${cliente}! Pedido recibido.`);
            localStorage.removeItem('mi_carrito_cafe');
            window.location.href = "index.html";
        } else {
            alert("Error al procesar pedido.");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error de conexión.");
    });
}