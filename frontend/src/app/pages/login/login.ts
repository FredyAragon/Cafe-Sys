import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.html'
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  // ✅ AQUÍ ESTABA EL ERROR: Faltaba declarar esta propiedad
  errorMessage: string | null = null; 

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required]
  });

  onSubmit() {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value as any).subscribe({
        next: () => this.router.navigate(['/admin/dashboard']),
        error: () => {
          // Actualizamos el valor de la variable cuando hay error
          this.errorMessage = 'Credenciales incorrectas o error de conexión';
        }
      });
    } else {
      this.loginForm.markAllAsTouched();
    }
  }
}