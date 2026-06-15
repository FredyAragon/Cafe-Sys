import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  standalone: true,
  selector: 'app-login',
  imports: [FormsModule],        // ✅ FormsModule para usar [(ngModel)] en el HTML
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {

  // Modelo del formulario
  email    = signal('');
  password = signal('');

  // Estado de la UI
  cargando = signal(false);
  error    = signal('');

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    // Validación básica antes de llamar a la API
    if (!this.email() || !this.password()) {
      this.error.set('Por favor ingresa tu email y contraseña.');
      return;
    }

    this.cargando.set(true);
    this.error.set('');

    this.authService.login({
      email: this.email(),
      password: this.password()
    }).subscribe({
      next: () => {
        // Login exitoso → vamos al dashboard
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.cargando.set(false);
        // Mostramos el mensaje de error que manda Django
        const msg = err?.error?.detail || 'Credenciales incorrectas. Intenta de nuevo.';
        this.error.set(msg);
      }
    });
  }
}
