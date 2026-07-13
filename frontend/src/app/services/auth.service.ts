import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, switchMap, map } from 'rxjs';
import { getApiUrl } from './api-config';

// ── Tipos que refleja exactamente lo que Django devuelve ──────────────────────
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface UsuarioSesion {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
  is_staff: boolean;
}

// ── Servicio ──────────────────────────────────────────────────────────────────
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly API_URL = 'http://127.0.0.1:8081/apps/core';

  // Guardamos los tokens en memoria (más seguro que localStorage para tokens de acceso)
  private _accessToken  = signal<string | null>(null);
  private _refreshToken = signal<string | null>(null);
  private _usuario      = signal<UsuarioSesion | null>(null);

  // Señal pública: ¿hay sesión activa?
  readonly estaAutenticado = computed(() => this._accessToken() !== null);

  // Señal pública: datos del usuario logueado
  readonly usuario = computed(() => this._usuario());

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    // Al iniciar la app, intentamos restaurar la sesión desde sessionStorage
    // (sessionStorage se borra al cerrar la pestaña — más seguro que localStorage)
    this._restaurarSesion();
  }

  // ── LOGIN ─────────────────────────────────────────────────────────────────
  login(credenciales: LoginCredentials): Observable<UsuarioSesion> {
    return this.http.post<AuthTokens>(`${this.API_URL}/token/`, credenciales).pipe(
      tap(tokens => {
        // Guardamos los tokens en memoria y sessionStorage
        this._guardarTokens(tokens);
      }),
      map(tokens => this._decodificarToken(tokens.access)),
      switchMap(payload => {
        if (!payload?.user_id) {
          throw new Error('Token inválido: falta user_id');
        }
        return this.http.get<UsuarioSesion>(`${this.API_URL}/users/${payload.user_id}/`);
      }),
      tap(usuario => {
        this._usuario.set(usuario);
        sessionStorage.setItem('cafesys_usuario', JSON.stringify(usuario));
      })
    );
  }

  // ── REGISTER ─────────────────────────────────────────────────────────────
  register(credenciales: RegisterCredentials): Observable<UsuarioSesion> {
    return this.http.post<UsuarioSesion>(`${this.API_URL}/users/`, credenciales);
  }

  // ── LOGOUT ────────────────────────────────────────────────────────────────
  logout(): void {
    // Limpiamos todo — memoria y sessionStorage
    this._accessToken.set(null);
    this._refreshToken.set(null);
    this._usuario.set(null);
    sessionStorage.clear();

    // Redirigimos al login
    this.router.navigate(['/login']);
  }

  // ── OBTENER TOKEN (lo usa el interceptor) ─────────────────────────────────
  getAccessToken(): string | null {
    return this._accessToken();
  }

  // ── REFRESH TOKEN ─────────────────────────────────────────────────────────
  refreshAccessToken(): Observable<AuthTokens> {
    const refresh = this._refreshToken();
    return this.http.post<AuthTokens>(`${this.API_URL}/token/refresh/`, { refresh }).pipe(
      tap(tokens => this._guardarTokens(tokens))
    );
  }

  // ── PRIVADOS ──────────────────────────────────────────────────────────────

  private _guardarTokens(tokens: AuthTokens): void {
    this._accessToken.set(tokens.access);
    this._refreshToken.set(tokens.refresh);
    // El refresh token sí lo guardamos en sessionStorage para sobrevivir recargas
    sessionStorage.setItem('cafesys_refresh', tokens.refresh);
    sessionStorage.setItem('cafesys_access', tokens.access);
  }

  private _restaurarSesion(): void {
    const access  = sessionStorage.getItem('cafesys_access');
    const refresh = sessionStorage.getItem('cafesys_refresh');
    const usuario = sessionStorage.getItem('cafesys_usuario');

    if (access && refresh) {
      // Verificamos que el token no haya expirado antes de restaurarlo
      if (!this._tokenExpirado(access)) {
        this._accessToken.set(access);
        this._refreshToken.set(refresh);
        if (usuario) {
          this._usuario.set(JSON.parse(usuario));
        }
      } else {
        // Token expirado — limpiamos todo para forzar login de nuevo
        sessionStorage.clear();
      }
    }
  }

  private _decodificarToken(token: string): any {
    try {
      const payload = token.split('.')[1];
      const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
      const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=');
      return JSON.parse(atob(padded));
    } catch {
      return null;
    }
  }

  private _tokenExpirado(token: string): boolean {
    const payload = this._decodificarToken(token);
    if (!payload?.exp) return true;
    // exp está en segundos, Date.now() en milisegundos
    return Date.now() >= payload.exp * 1000;
  }
}