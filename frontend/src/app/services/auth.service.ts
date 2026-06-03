import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // La URL base la toma directo del environment que creamos
  private apiUrl = environment.apiUrl; 

  constructor(private http: HttpClient) {}

  // 🚀 POST: Mandar credenciales y recibir el JWT
  login(credentials: { email: string; password: string }) {
    return this.http.post<{ access: string; refresh: string }>(`${this.apiUrl}token/`, credentials).pipe(
      tap(response => {
        // Guardamos los tokens de forma segura en el almacenamiento local del navegador
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
      })
    );
  }

  // Método auxiliar para recuperar el token guardado
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }
}