import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { roleGuard } from './guards/role.guard';

export const routes: Routes = [
  // Redirección por defecto
  { path: '', redirectTo: 'tienda', pathMatch: 'full' },

  // ==========================================
  // ZONA PÚBLICA / CLIENTES (Layout Cliente)
  // ==========================================
  {
    path: 'tienda',
    loadComponent: () => import('./pages/layouts/app-layout/app-layout').then(m => m.ClientLayoutComponent),
    children: [
      { path: '', loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent) },
    ]
  },

  // ==========================================
  // ZONA ADMINISTRATIVA (Layout Admin)
  // ==========================================
  {
    path: 'admin',
    loadComponent: () => import('./pages/layouts/admin-layout/admin-layout').then(m => m.AdminLayoutComponent),
    canActivate: [authGuard, roleGuard], // Protegido por sesión y por rol
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.DashboardComponent) },
      { path: 'products', loadComponent: () => import('./pages/products/products').then(m => m.ProductsComponent) },
      { path: 'categories', loadComponent: () => import('./pages/categories/categories').then(m => m.CategoriesComponent) },
    ]
  },

  // ==========================================
  // AUTENTICACIÓN (Sin Layout, vista limpia)
  // ==========================================
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.LoginComponent)
  },

  // Ruta fallback para URLs no encontradas
  { path: '**', redirectTo: 'tienda' }
];