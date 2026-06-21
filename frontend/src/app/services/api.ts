import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, timeout } from 'rxjs';

// ── Tipos básicos que devuelve Django ──────────────────────────────────────
export interface Categoria {
  id: number;
  name: string;
  description: string | null;
  imageUrl: string | null;
  status: string;
}

export interface NuevaCategoria {
  name: string;
  description?: string;
  imageUrl?: string;
  status?: string;
}

export interface Producto {
  id: number;
  name: string;
  description: string | null;
  price: string;          // DRF serializa DecimalField como string
  imageUrl: string | null;
  category: number;
  category_name: string;
  status: string;
}

export interface NuevoProducto {
  name: string;
  description?: string;
  price: number;
  imageUrl?: string;
  category: number;
  status?: string;
}

// ── Órdenes ─────────────────────────────────────────────────────────────────
export interface OrderDetailData {
  product: number;
  quantity: number;
  unitPrice: number;
}

export interface NewOrder {
  user: number;
  location: number;
  orderStatus: string;
  total: number;
  notes?: string;
  details_data?: OrderDetailData[];
}

export interface ProductDetail {
  id: number;
  name: string;
  price: string;
  imageUrl: string | null;
  status: string;
}

/** Formato plano devuelto por GET /order-details/ */
export interface OrderDetailFlat {
  id: number;
  order: number;
  product: number;
  product_name: string;
  quantity: number;
  unitPrice: string;
  subtotal: string;
  status: string;
  created: string;
  modified: string;
}

/** Formato anidado dentro de una orden (GET /orders/) */
export interface OrderDetailNested {
  id: number;
  product: number;
  product_detail: ProductDetail;
  quantity: number;
  unitPrice: string;
  subtotal: string;
  status: string;
}

export interface UserDetail {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  role: string;
  status: string;
}

export interface Order {
  id: number;
  user: number;
  user_detail: UserDetail;
  location: number;
  orderStatus: string;
  total: string;
  notes: string | null;
  details: OrderDetailNested[];
  status: string;
  created: string;
  modified: string;
}

// ── Ubicaciones ─────────────────────────────────────────────────────────────
export interface Ubicacion {
  id: number;
  user: number;
  alias: string;
  address: string;
  reference: string | null;
  isDefault: boolean;
  status: string;
  created: string;
  modified: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private readonly API_URL = `http://${this.getBackendHost()}:8081/apps/core`;

  /** Tiempo máximo de espera para cada petición (ms) */
  private readonly TIMEOUT = 10_000;

  constructor(private readonly http: HttpClient) {}

  private getBackendHost(): string {
    if (typeof window === 'undefined') {
      return '127.0.0.1';
    }
    const hostname = window.location.hostname;
    return hostname === 'localhost' || hostname === '127.0.0.1' ? '127.0.0.1' : 'host.docker.internal';
  }

  // ── PRODUCTOS ─────────────────────────────────────────────────────────────
  getProducts(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.API_URL}/products/`).pipe(timeout(this.TIMEOUT));
  }

  createProduct(productData: NuevoProducto): Observable<Producto> {
    return this.http.post<Producto>(`${this.API_URL}/products/`, productData).pipe(timeout(this.TIMEOUT));
  }

  updateProduct(id: number, productData: Partial<NuevoProducto>): Observable<Producto> {
    return this.http.patch<Producto>(`${this.API_URL}/products/${id}/`, productData).pipe(timeout(this.TIMEOUT));
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/products/${id}/`).pipe(timeout(this.TIMEOUT));
  }

  // ── CATEGORÍAS ────────────────────────────────────────────────────────────
  getCategories(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.API_URL}/categories/`).pipe(timeout(this.TIMEOUT));
  }

  createCategory(categoryData: NuevaCategoria): Observable<Categoria> {
    return this.http.post<Categoria>(`${this.API_URL}/categories/`, categoryData).pipe(timeout(this.TIMEOUT));
  }

  updateCategory(id: number, categoryData: Partial<NuevaCategoria>): Observable<Categoria> {
    return this.http.patch<Categoria>(`${this.API_URL}/categories/${id}/`, categoryData).pipe(timeout(this.TIMEOUT));
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/categories/${id}/`).pipe(timeout(this.TIMEOUT));
  }

  // ── UBICACIONES ───────────────────────────────────────────────────────────
  getLocations(): Observable<Ubicacion[]> {
    return this.http.get<Ubicacion[]>(`${this.API_URL}/locations/`).pipe(timeout(this.TIMEOUT));
  }

  createLocation(locationData: { user: number; alias: string; address: string; reference?: string; isDefault?: boolean }): Observable<Ubicacion> {
    return this.http.post<Ubicacion>(`${this.API_URL}/locations/`, locationData).pipe(timeout(this.TIMEOUT));
  }

  // ── ÓRDENES ───────────────────────────────────────────────────────────────
  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.API_URL}/orders/`).pipe(timeout(this.TIMEOUT));
  }

  createOrder(orderData: NewOrder): Observable<Order> {
    return this.http.post<Order>(`${this.API_URL}/orders/`, orderData).pipe(timeout(this.TIMEOUT));
  }

  // ── DETALLES DE ÓRDENES ───────────────────────────────────────────────────
  getOrderDetails(): Observable<OrderDetailFlat[]> {
    return this.http.get<OrderDetailFlat[]>(`${this.API_URL}/order-details/`).pipe(timeout(this.TIMEOUT));
  }

  createOrderDetail(detailData: { order: number; product: number; quantity: number; unitPrice: number }): Observable<OrderDetailFlat> {
    return this.http.post<OrderDetailFlat>(`${this.API_URL}/order-details/`, detailData).pipe(timeout(this.TIMEOUT));
  }
}
