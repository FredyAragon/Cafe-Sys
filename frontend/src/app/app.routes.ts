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
        { path: 'menu', loadComponent: () => import('./pages/menu/menu').then(m => m.MenuComponent) },
        { path: 'carrito', loadComponent: () => import('./pages/cart/cart').then(m => m.CartComponent) },
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
      { path: 'productos', loadComponent: () => import('./pages/products/products').then(m => m.ProductsComponent), data: { adminOnly: true } },
      { path: 'categorias', loadComponent: () => import('./pages/categories/categories').then(m => m.CategoriesComponent), data: { adminOnly: true } },
      { path: 'ordenes', loadComponent: () => import('./pages/admin/ordenes/ordenes').then(m => m.OrdenesComponent) },
      { path: 'usuarios', loadComponent: () => import('./pages/admin/users/users').then(m => m.UsersComponent), data: { adminOnly: true } },
    ]
  },

  // ==========================================
  // ÓRDENES PÚBLICAS (Sin autenticación, solo lectura)
  // ==========================================
  {
    path: 'ordenes',
    loadComponent: () => import('./pages/admin/ordenes/ordenes').then(m => m.OrdenesComponent)
  },

  // ==========================================
  // AUTENTICACIÓN (Sin Layout, vista limpia)
  // ==========================================
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register').then(m => m.RegisterComponent)
  },
  // Ruta fallback para URLs no encontradas
  { path: '**', redirectTo: 'tienda' }
];