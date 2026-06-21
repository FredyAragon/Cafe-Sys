import { Component, inject, computed } from '@angular/core';
import { NgIf } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-admin-layout',
  standalone: true,
  imports: [NgIf, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './admin-layout.html',
  styleUrls: ['./admin-layout.css']
})
export class AdminLayoutComponent {
  private authService = inject(AuthService);
  usuario = this.authService.usuario; // Exponemos la señal al template

  mostrarOrdenes = computed(() => {
    const role = this.usuario()?.role ?? '';
    return role === 'Driver' || role === 'Employee';
  });

  cerrarSesion() {
    this.authService.logout();
  }
}