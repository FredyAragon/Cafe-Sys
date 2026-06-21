import { Component, inject } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';

// ✅ Este componente envuelve todas las páginas protegidas (dashboard, products, categories).
//    Contiene la barra superior con navegación, datos del usuario y logout,
//    para que no haya que repetirla en cada página.
@Component({
  standalone: true,
  selector: 'app-layout',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './layout.html',
  styleUrls: ['./layout.css']
})
export class LayoutComponent {
  private authService = inject(AuthService);

  usuario = this.authService.usuario;

  cerrarSesion() {
    this.authService.logout();
  }
}
