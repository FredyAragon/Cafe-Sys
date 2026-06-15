import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

/**
 * Guard funcional (estilo moderno de Angular, sin clases).
 * Se usa en app.routes.ts con: canActivate: [authGuard]
 *
 * Si el usuario NO está autenticado, lo redirige a /login
 * y bloquea el acceso a la ruta protegida.
 */
export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.estaAutenticado()) {
    return true;
  }

  // No hay sesión activa → redirigir a login
  router.navigate(['/login']);
  return false;
};
