import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Order } from '../../../services/api';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-ordenes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ordenes.html',
  styleUrls: ['./ordenes.css']
})
export class OrdenesComponent implements OnInit {
  private apiService = inject(ApiService);
  private authService = inject(AuthService);

  orders = signal<Order[]>([]);
  cargando = signal(false);
  error = signal('');
  sortKey: string = 'id';
  sortDir: 'asc' | 'desc' = 'asc';
  usuario = this.authService.usuario;
  puedeGestionar = computed(() => {
    const role = this.usuario()?.role ?? '';
    return this.usuario()?.is_staff || role === 'Employee' || role === 'Driver';
  });

  ngOnInit() {
    this.loadOrders();
  }

  sortOrders(columna: string): void {
    if (this.sortKey === columna) {
      this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = columna;
      this.sortDir = 'asc';
    }
    this.applyOrderSort();
  }

  private applyOrderSort() {
    const key = this.sortKey as keyof Order;
    const dir = this.sortDir;
    const numericKeys: Array<keyof Order> = ['id'];
    this.orders.update((list: Order[]) => {
      const sorted = [...list].sort((a, b) => {
        const forceNumeric = numericKeys.includes(key);
        const aVal = (a as any)[key];
        const bVal = (b as any)[key];
        if (forceNumeric) {
          const numA = Number(aVal) || 0;
          const numB = Number(bVal) || 0;
          return dir === 'asc' ? numA - numB : numB - numA;
        }
        const strA = (String(aVal ?? '')).toLowerCase();
        const strB = (String(bVal ?? '')).toLowerCase();
        if (strA < strB) return dir === 'asc' ? -1 : 1;
        if (strA > strB) return dir === 'asc' ? 1 : -1;
        return 0;
      });
      return sorted;
    });
  }

  loadOrders() {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getOrders().subscribe({
      next: (data: Order[]) => {
        // Filtrar órdenes archivadas (inactive) para que no aparezcan
        const filtered = data.filter(o => o.status !== 'inactive');
        this.orders.set(filtered);
        this.applyOrderSort();
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar pedidos:', err);
        this.error.set('No se pudieron cargar los pedidos.');
        this.cargando.set(false);
      }
    });
  }

  avanzarEstado(orderId: number) {
    this.apiService.advanceOrderStatus(orderId).subscribe({
      next: () => this.loadOrders(),
      error: (err: any) => {
        console.error('Error al actualizar pedido:', err);
        this.error.set('No se pudo actualizar el estado de la orden.');
      }
    });
  }

  archivarOrden(orderId: number) {
    this.apiService.archiveOrder(orderId).subscribe({
      next: () => this.loadOrders(),
      error: (err: any) => {
        console.error('Error al archivar orden:', err);
        this.error.set('No se pudo archivar la orden.');
      }
    });
  }
}