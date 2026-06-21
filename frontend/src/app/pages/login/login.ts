import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private router = inject(Router);

  // Definimos el formulario con sus validaciones
  loginForm: FormGroup = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]]
  });

  errorMessage: string | null = null;

  onSubmit() {
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value;
      console.log('Datos listos para enviar al backend:', email);
      
      // TODO: Aquí conectaremos con nuestro AuthService para obtener el JWT.
      // Por ahora, para probar la ruta, simularemos una redirección al panel de admin:
      this.router.navigate(['/admin/dashboard']);
      
    } else {
      // Si el formulario es inválido, marcamos todos los campos para mostrar los errores visuales
      this.loginForm.markAllAsTouched();
    }
  }
}