import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent {
  private authService = inject(AuthService);

  usuario = this.authService.usuario;

  estadisticas = [
    { titulo: 'Ventas de hoy', valor: 'S/ 0.00' },
    { titulo: 'Ordenes pendientes', valor: '0' },
    { titulo: 'Productos activos', valor: '0' },
    { titulo: 'Clientes registrados', valor: '0' }
  ];
}
