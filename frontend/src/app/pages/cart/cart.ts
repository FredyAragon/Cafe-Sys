import { Component, inject, signal, computed } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CartService, CartItem } from '../../services/cart.service';
import { ApiService, Order, OrderDetail } from '../../services/api';
import { AuthService } from '../../services/auth.service';

@Component({
  standalone: true,
  selector: 'app-cart',
  imports: [CommonModule, RouterLink],
  templateUrl: './cart.html',
  styleUrls: ['./cart.css']
})
export class CartComponent {
  private cartService = inject(CartService);
  private apiService = inject(ApiService);
  private authService = inject(AuthService);
  private router = inject(Router);

  /** Expuesto para usar Number() en el template */
  Number = Number;

  items = this.cartService.items;
  total = this.cartService.total;
  count = this.cartService.count;

  usuario = this.authService.usuario;

  guardando = signal(false);
  compraExitosa = signal(false);
  error = signal('');
  ordenCreada = signal<Order | null>(null);

  actualizarCantidad(productId: number, cantidad: number) {
    this.cartService.updateQuantity(productId, cantidad);
  }

  eliminar(productId: number) {
    this.cartService.removeProduct(productId);
  }

  vaciarCarrito() {
    this.cartService.clear();
  }

  finalizarCompra() {
    const user = this.usuario();
    if (!user) {
      this.error.set('Debes iniciar sesión para comprar.');
      return;
    }

    const cartItems = this.items();
    if (cartItems.length === 0) {
      this.error.set('El carrito está vacío.');
      return;
    }

    this.error.set('');
    this.guardando.set(true);

    // 1. Crear la orden
    const orderPayload = {
      user: user.id,
      location: 1,  // ubicación por defecto; idealmente el usuario la elige
      orderStatus: 'pending' as const,
      total: this.total(),
      notes: ''
    };

    this.apiService.createOrder(orderPayload).subscribe({
      next: (order) => {
        // 2. Crear los detalles de la orden
        const detailCalls = cartItems.map(item =>
          this.apiService.createOrderDetail({
            order: order.id,
            product: item.product.id,
            quantity: item.quantity,
            unitPrice: Number(item.product.price)
          })
        );

        // Ejecutamos todos en paralelo
        let completed = 0;
        detailCalls.forEach(call$ => {
          call$.subscribe({
            next: () => {
              completed++;
              if (completed === detailCalls.length) {
                // Todos los detalles creados
                this.ordenCreada.set(order);
                this.compraExitosa.set(true);
                this.guardando.set(false);
                this.cartService.clear();
              }
            },
            error: (err) => {
              this.guardando.set(false);
              this.error.set('Error al crear los detalles de la orden.');
              console.error('Error creating order detail:', err);
            }
          });
        });
      },
      error: (err) => {
        this.guardando.set(false);
        this.error.set('Error al crear la orden. Intenta de nuevo.');
        console.error('Error creating order:', err);
      }
    });
  }

  irMenu() {
    this.router.navigate(['/tienda/menu']);
  }

  irMisOrdenes() {
    this.router.navigate(['/tienda']);
  }
}
