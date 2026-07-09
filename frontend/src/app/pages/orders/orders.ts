import { Component, OnInit, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// ── Tipos ─────────────────────────────────────────────────────────────────
interface DetallePedido {
  id: number;
  product: number;
  product_name: string;
  quantity: number;
  unitPrice: string;
  subtotal: string;
}

interface Pedido {
  id: number;
  user: number;
  user_detail: { firstName: string; lastName: string; email: string };
  location: number;
  orderStatus: string;
  total: string;
  notes: string | null;
  details: DetallePedido[];
  status: string;
  created: string;
}

// ── Flujo de estados ──────────────────────────────────────────────────────
// Define el estado siguiente permitido para cada estado actual.
// Si el valor es null, ese estado es terminal (no avanza mas).
const FLUJO: Record<string, string | null> = {
  pending:   'preparing',
  preparing: 'ready',
  ready:     'delivered',
  delivered: null,
  cancelled: null
};

// Textos legibles en espanol para mostrar en la UI
const ETIQUETAS: Record<string, string> = {
  pending:   'Pendiente',
  preparing: 'En preparacion',
  ready:     'Listo',
  delivered: 'Entregado',
  cancelled: 'Cancelado'
};

// Texto del boton de avance para cada estado
const BOTON_AVANCE: Record<string, string> = {
  pending:   'Aceptar pedido',
  preparing: 'Marcar como listo',
  ready:     'Marcar como entregado',
};

@Component({
  standalone: true,
  selector: 'app-orders',
  imports: [],
  templateUrl: './orders.html',
  styleUrls: ['./orders.css']
})
export class OrdersComponent implements OnInit {

  private http = inject(HttpClient);
  private readonly API_URL = 'http://127.0.0.1:8000/apps/core';

  // ── Datos ───────────────────────────────────────────────────────────────
  pedidos = signal<Pedido[]>([]);

  // ── Estado de la UI ─────────────────────────────────────────────────────
  cargando = signal(false);
  mensaje = signal('');
  error = signal('');
  expandidoId = signal<number | null>(null);
  actualizandoId = signal<number | null>(null);

  // ── Filtro activo ────────────────────────────────────────────────────────
  filtro = signal<string>('todos');

  ngOnInit() {
    this.cargarPedidos();
  }

  cargarPedidos() {
    this.cargando.set(true);
    this.error.set('');
    this.http.get<Pedido[]>(`${this.API_URL}/orders/`).subscribe({
      next: (data) => {
        this.pedidos.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los pedidos.');
        this.cargando.set(false);
      }
    });
  }

  // ── Computed: pedidos filtrados por estado ───────────────────────────────
  pedidosFiltrados(): Pedido[] {
    if (this.filtro() === 'todos') return this.pedidos();
    return this.pedidos().filter(p => p.orderStatus === this.filtro());
  }

  // ── Contadores por estado (para las pestanas) ───────────────────────────
  contarPor(estado: string): number {
    if (estado === 'todos') return this.pedidos().length;
    return this.pedidos().filter(p => p.orderStatus === estado).length;
  }

  // ── Helpers expuestos al template ────────────────────────────────────────
  etiqueta(estado: string): string {
    return ETIQUETAS[estado] ?? estado;
  }

  siguienteEstado(estado: string): string | null {
    return FLUJO[estado] ?? null;
  }

  textBotonAvance(estado: string): string {
    return BOTON_AVANCE[estado] ?? 'Avanzar';
  }

  puedeCancel(estado: string): boolean {
    return estado === 'pending' || estado === 'preparing';
  }

  toggleDetalle(p: Pedido) {
    this.expandidoId.set(this.expandidoId() === p.id ? null : p.id);
  }

  // ── Helpers para el flujo visual de pasos ────────────────────────────────
  // Orden de los pasos (sin 'cancelled')
  private readonly ORDEN = ['pending', 'preparing', 'ready', 'delivered'];

  esPasoCompletado(estadoActual: string, paso: string): boolean {
    if (estadoActual === 'cancelled') return false;
    const idxActual = this.ORDEN.indexOf(estadoActual);
    const idxPaso   = this.ORDEN.indexOf(paso);
    // Un paso esta completado si ya se paso de el (el actual es posterior)
    return idxPaso < idxActual;
  }

  esPasoPendiente(estadoActual: string, paso: string): boolean {
    if (estadoActual === 'cancelled') return true;
    const idxActual = this.ORDEN.indexOf(estadoActual);
    const idxPaso   = this.ORDEN.indexOf(paso);
    return idxPaso > idxActual;
  }

  formatearFecha(iso: string): string {
    return new Date(iso).toLocaleString('es-PE', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  // ── Cambio de estado: avanzar al siguiente en el flujo ───────────────────
  avanzarEstado(p: Pedido) {
    const siguiente = FLUJO[p.orderStatus];
    if (!siguiente) return;
    this.cambiarEstado(p, siguiente);
  }

  // ── Cambio de estado: cancelar ───────────────────────────────────────────
  cancelarPedido(p: Pedido) {
    const confirmado = confirm(
      `Cancelar el pedido #${p.id} de ${p.user_detail.firstName} ${p.user_detail.lastName}?\nEsta accion no se puede deshacer.`
    );
    if (!confirmado) return;
    this.cambiarEstado(p, 'cancelled');
  }

  // ── Logica central de cambio de estado ───────────────────────────────────
  private cambiarEstado(p: Pedido, nuevoEstado: string) {
    this.error.set('');
    this.mensaje.set('');
    this.actualizandoId.set(p.id);

    this.http.patch<Pedido>(
      `${this.API_URL}/orders/${p.id}/`,
      { orderStatus: nuevoEstado }
    ).subscribe({
      next: (actualizado) => {
        this.pedidos.update(actuales =>
          actuales.map(item => item.id === actualizado.id ? actualizado : item)
        );
        this.mensaje.set(
          `Pedido #${actualizado.id} actualizado a "${this.etiqueta(actualizado.orderStatus)}".`
        );
        this.actualizandoId.set(null);
      },
      error: () => {
        this.actualizandoId.set(null);
        this.error.set(`No se pudo actualizar el pedido #${p.id}.`);
      }
    });
  }
}
