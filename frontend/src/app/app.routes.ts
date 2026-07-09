import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';
import { LayoutComponent } from './pages/layout/layout';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { ProductsComponent } from './pages/products/products';
import { CategoriesComponent } from './pages/categories/categories';
import { OrdersComponent } from './pages/orders/orders';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },

  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'products', component: ProductsComponent },
      { path: 'categories', component: CategoriesComponent },
      { path: 'orders', component: OrdersComponent },
    ]
  },

  { path: '**', redirectTo: 'dashboard' }
];
