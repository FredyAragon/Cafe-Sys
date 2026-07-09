import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const usuario = authService.usuario(); // Leemos la señal del usuario

  if (!usuario) {
    return router.createUrlTree(['/login']);
  }

  const allowedAdminLayoutRoles = ['Admin', 'Driver', 'Employee'];

  if (!usuario.is_staff && !allowedAdminLayoutRoles.includes(usuario.role)) {
    return router.createUrlTree(['/tienda']);
  }

  const adminOnly = (route.data?.['adminOnly'] ?? route.firstChild?.data?.['adminOnly']) as boolean | undefined;
  const driverEmployeeOnly = (route.data?.['driverEmployeeOnly'] ?? route.firstChild?.data?.['driverEmployeeOnly']) as boolean | undefined;

  if (adminOnly && usuario.role !== 'Admin') {
    return router.createUrlTree(['/admin/dashboard']);
  }

  if (driverEmployeeOnly && !['Driver', 'Employee'].includes(usuario.role)) {
    return router.createUrlTree(['/admin/dashboard']);
  }

  return true;
};
