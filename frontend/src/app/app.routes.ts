import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';
import { LayoutComponent } from './pages/layout/layout';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { ProductsComponent } from './pages/products/products';
import { CategoriesComponent } from './pages/categories/categories';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // Login (pública, sin layout)
  { path: 'login', component: LoginComponent },

  // ✅ Todas las rutas internas comparten el Layout (topbar + navegación)
  //    y están protegidas por authGuard a nivel de padre — se aplica a todas
  //    las hijas automáticamente.
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'products', component: ProductsComponent },
      { path: 'categories', component: CategoriesComponent },
    ]
  },

  // Cualquier ruta no reconocida → vuelve a dashboard (y el guard decide)
  { path: '**', redirectTo: 'dashboard' }
];
