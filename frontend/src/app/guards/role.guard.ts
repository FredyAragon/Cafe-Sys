import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const usuario = authService.usuario(); // Leemos la señal del usuario

  // Verificamos si el usuario existe y si es parte del staff (admin)
  if (usuario && usuario.is_staff) {
    return true;
  }

  // Si es un cliente normal o alguien sin permisos, lo redirigimos a la tienda
  return router.createUrlTree(['/tienda']);
};