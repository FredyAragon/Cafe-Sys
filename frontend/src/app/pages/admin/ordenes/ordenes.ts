import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Order } from '../../../services/api';

@Component({
  selector: 'app-ordenes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ordenes.html',
  styleUrls: ['./ordenes.css']
})
export class OrdenesComponent implements OnInit {
  private apiService = inject(ApiService);

  orders = signal<Order[]>([]);
  cargando = signal(false);
  error = signal('');

  ngOnInit() {
    this.loadOrders();
  }

  loadOrders() {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getOrders().subscribe({
      next: (data: Order[]) => {
        this.orders.set(data);
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar pedidos:', err);
        this.error.set('No se pudieron cargar los pedidos.');
        this.cargando.set(false);
      }
    });
  }
}