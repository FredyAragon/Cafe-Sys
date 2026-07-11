import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CartService, CartItem } from '../../services/cart.service';
import { ApiService, Order, Ubicacion } from '../../services/api';
import { AuthService } from '../../services/auth.service';

@Component({
  standalone: true,
  selector: 'app-cart',
<<<<<<< HEAD
  imports: [CommonModule],
=======
  imports: [CommonModule, RouterLink],
>>>>>>> Jose
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

  /** Obtiene o crea una ubicación por defecto para el usuario */
  private obtenerUbicacion(userId: number): Promise<number> {
    return new Promise((resolve, reject) => {
      this.apiService.getLocations().subscribe({
        next: (locations: Ubicacion[]) => {
          const delUsuario = locations.filter(l => l.user === userId && l.status === 'active');
          if (delUsuario.length > 0) {
            resolve(delUsuario[0].id);
          } else {
            // Crear una ubicación por defecto
            this.apiService.createLocation({
              user: userId,
              alias: 'Mi dirección',
              address: 'Dirección por defecto',
              isDefault: true
            }).subscribe({
              next: (loc: Ubicacion) => resolve(loc.id),
              error: (err: any) => reject(err)
            });
          }
        },
        error: (err: any) => reject(err)
      });
    });
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

    // 1. Obtener ubicación del usuario
    this.obtenerUbicacion(user.id).then((locationId) => {
      // 2. Construir details_data a partir del carrito
      const detailsData = cartItems.map((item: CartItem) => ({
        product: item.product.id,
        quantity: item.quantity,
        unitPrice: Number(item.product.price)
      }));

      // 3. Crear la orden con sus detalles en una sola llamada atómica
      this.apiService.createOrder({
        user: user.id,
        location: locationId,
        orderStatus: 'pending',
        total: this.total(),
        notes: '',
        details_data: detailsData
      }).subscribe({
        next: (order: Order) => {
          this.ordenCreada.set(order);
          this.compraExitosa.set(true);
          this.cartService.clear();
          this.guardando.set(false);
        },
        error: (err: any) => {
          this.guardando.set(false);
          const detail = err?.error;
          if (detail && typeof detail === 'object') {
            const firstKey = Object.keys(detail)[0];
            const firstMsg = Array.isArray(detail[firstKey]) ? detail[firstKey][0] : detail[firstKey];
            this.error.set(`${firstKey}: ${firstMsg}`);
          } else {
            this.error.set(`Error del servidor: ${err.status} - ${err.statusText}`);
          }
          console.error('Error creando orden con detalles:', err);
        }
      });
    }).catch((err: any) => {
      this.guardando.set(false);
      const detail = err?.error;
      if (detail && typeof detail === 'object') {
        const firstKey = Object.keys(detail)[0];
        const firstMsg = Array.isArray(detail[firstKey]) ? detail[firstKey][0] : detail[firstKey];
        this.error.set(`${firstKey}: ${firstMsg}`);
      } else {
        this.error.set('Error al obtener ubicación. Revisa tu perfil.');
      }
      console.error('Error en obtenerUbicacion:', err);
    });
  }

  irMenu() {
    this.router.navigate(['/tienda/menu']);
  }

  irMisOrdenes() {
    this.router.navigate(['/tienda']);
  }
}