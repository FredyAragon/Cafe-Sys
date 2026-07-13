import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, Order } from '../../services/api';
import { AuthService, UsuarioSesion } from '../../services/auth.service';

@Component({
  selector: 'app-mis-pedidos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mis-pedidos.html',
  styleUrls: ['./mis-pedidos.css']
})
export class MisPedidosComponent implements OnInit {
  private apiService = inject(ApiService);
  private authService = inject(AuthService);

  usuario = this.authService.usuario;
  orders = signal<Order[]>([]);
  cargando = signal(false);
  error = signal('');
  cancelandoId = signal<number | null>(null);

  // Review state
  reviewForm = signal<{ orderId: number; productName: string; rating: number; comment: string } | null>(null);
  enviandoReview = signal(false);
  reviewExito = signal('');
  reviewError = signal('');
  reviewsEnviadas = signal<Set<number>>(new Set());

  statusLabels: Record<string, string> = {
    pending: 'Pendiente',
    assigned: 'Asignada',
    preparing: 'Preparando',
    ready: 'Lista',
    delivered: 'Entregada',
    cancelled: 'Cancelada'
  };

  statusColors: Record<string, string> = {
    pending: '#E65100',
    assigned: '#7C3AED',
    preparing: '#1565C0',
    ready: '#0F766E',
    delivered: '#2E7D32',
    cancelled: '#C62828'
  };

  ngOnInit() {
    this.loadMisPedidos();
  }

  loadMisPedidos() {
    const user = this.usuario();
    if (!user) return;

    this.cargando.set(true);
    this.error.set('');

    this.apiService.getOrders().subscribe({
      next: (data: Order[]) => {
        // Filtrar solo las órdenes del usuario actual
        const misOrdenes = data.filter(o => o.user === user.id);
        this.orders.set(misOrdenes);
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar pedidos:', err);
        this.error.set('No se pudieron cargar tus pedidos.');
        this.cargando.set(false);
      }
    });
  }

  cancelarOrden(orderId: number) {
    this.cancelandoId.set(orderId);
    this.error.set('');

    this.apiService.cancelOrder(orderId).subscribe({
      next: () => {
        this.cancelandoId.set(null);
        this.loadMisPedidos();
      },
      error: (err: any) => {
        this.cancelandoId.set(null);
        const detail = err?.error?.detail || 'No se pudo cancelar la orden.';
        this.error.set(detail);
        console.error('Error al cancelar orden:', err);
      }
    });
  }

  puedeCancelar(order: Order): boolean {
    return order.orderStatus === 'pending' && order.status !== 'inactive';
  }

  puedeDejarResena(order: Order): boolean {
    return order.orderStatus === 'delivered';
  }

  abrirReviewForm(orderId: number, productName: string) {
    if (this.reviewsEnviadas().has(orderId)) return;

    this.reviewForm.set({ orderId, productName, rating: 5, comment: '' });
    this.reviewExito.set('');
    this.reviewError.set('');
  }

  cerrarReviewForm() {
    this.reviewForm.set(null);
  }

  enviarReview() {
    const form = this.reviewForm();
    const user = this.usuario();
    if (!form || !user) return;

    this.enviandoReview.set(true);
    this.reviewError.set('');
    this.reviewExito.set('');

    this.apiService.createReview({
      user: user.id,
      order: form.orderId,
      rating: form.rating,
      comment: form.comment
    }).subscribe({
      next: () => {
        this.enviandoReview.set(false);
        this.reviewsEnviadas.update((s: Set<number>) => new Set(s).add(form.orderId));
        this.reviewExito.set(`Reseña enviada para "${form.productName}"`);
        setTimeout(() => {
          this.reviewForm.set(null);
          this.reviewExito.set('');
        }, 2000);
      },
      error: (err: any) => {
        this.enviandoReview.set(false);
        const detail = err?.error;
        if (detail && typeof detail === 'object') {
          const firstKey = Object.keys(detail)[0];
          const firstMsg = Array.isArray(detail[firstKey]) ? detail[firstKey][0] : detail[firstKey];
          this.reviewError.set(`${firstKey}: ${firstMsg}`);
        } else {
          this.reviewError.set('Error al enviar la reseña.');
        }
        console.error('Error al crear reseña:', err);
      }
    });
  }

  yaTieneReview(orderId: number): boolean {
    return this.reviewsEnviadas().has(orderId);
  }
}