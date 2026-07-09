import { Component, inject } from '@angular/core';
import { NgIf } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { CartService } from '../../../services/cart.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [NgIf, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-layout.html',
  styleUrls: ['./app-layout.css']
})
export class ClientLayoutComponent {
  private authService = inject(AuthService);
  private cartService = inject(CartService);
  usuario = this.authService.usuario;
  cartCount = this.cartService.count;

  cerrarSesion() {
    this.authService.logout();
  }
}
