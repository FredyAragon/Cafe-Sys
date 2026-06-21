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
  
  // Leemos el usuario actual para darle una bienvenida personalizada
  usuario = this.authService.usuario;

  // Datos simulados para la maqueta
  estadisticas = [
    { titulo: 'Ventas de hoy', valor: 'S/ 0.00', icono: '💰' },
    { titulo: 'Órdenes pendientes', valor: '0', icono: '📦' },
    { titulo: 'Productos activos', valor: '0', icono: '☕' },
    { titulo: 'Nuevos clientes', valor: '0', icono: '👥' }
  ];
}