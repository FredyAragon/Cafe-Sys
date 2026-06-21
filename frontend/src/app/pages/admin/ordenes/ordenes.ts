import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../services/api';

export interface OrderDetail {
  id: number;
  order: number;
  product: number;
  product_name: string;
  quantity: number;
  unitPrice: string;
  subtotal: string;
  status: string;
  created: string;
  modified: string;
}

@Component({
  selector: 'app-ordenes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ordenes.html',
  styleUrls: ['./ordenes.css']
})
export class OrdenesComponent implements OnInit {
  private apiService = inject(ApiService);

  orderDetails = signal<OrderDetail[]>([]);
  cargando = signal(false);
  error = signal('');

  ngOnInit() {
    this.loadOrderDetails();
  }

  loadOrderDetails() {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getOrderDetails().subscribe({
      next: (data) => {
        this.orderDetails.set(data);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar detalles de pedido:', err);
        this.error.set('No se pudieron cargar los detalles de pedido.');
        this.cargando.set(false);
      }
    });
  }
}
