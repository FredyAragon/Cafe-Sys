import { Component, inject } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-layout.html',
  styleUrls: ['./app-layout.css']
})
export class ClientLayoutComponent {
  private authService = inject(AuthService);
  usuario = this.authService.usuario;

  cerrarSesion() {
    this.authService.logout();
  }
}