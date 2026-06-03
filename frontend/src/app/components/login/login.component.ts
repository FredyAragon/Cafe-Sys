import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../services/auth.service'; // Sube dos niveles hasta services
import { environment } from '../../../environments/environment'; // Sube tres niveles hasta src

@Component({
  selector: 'app-login',
  standalone: true, // Importante en Angular moderno
  template: `
    <div style="padding: 20px; text-align: center;">
      <h2>Prueba de Conexión CafeSys</h2>
      <button (click)="probarFlujoCompleto()" style="padding: 10px 20px; cursor: pointer;">
        Disparar POST (Login) y GET (Roles)
      </button>
    </div>
  `
})
export class LoginComponent {

  constructor(private authService: AuthService, private http: HttpClient) {}

  probarFlujoCompleto() {
    const credencialesPrueba = {
      email: 'cliente_prueba@cafesys.com',
      password: 'PasswordSeguro123!'
    };

    console.log('🚀 1. Enviando POST para login...');
    
    this.authService.login(credencialesPrueba).subscribe({
      next: (tokens) => {
        console.log('✅ POST Exitoso. Tokens en LocalStorage:', tokens);

        // Al recibir el OK, disparamos inmediatamente el GET protegido
        console.log('🔍 2. Enviando GET protegido a /roles/...');
        this.http.get(`${environment.apiUrl}roles/`).subscribe({
          next: (roles) => {
            console.log('🎉 ¡GET Exitoso! Datos protegidos recibidos:', roles);
          },
          error: (err) => {
            console.error('❌ Error en el GET protegido. ¿Falta CORS en Django?:', err);
          }
        });

      },
      error: (err) => {
        console.error('❌ Error en el POST de login. Revisa credenciales o CORS:', err);
      }
    });
  }
}