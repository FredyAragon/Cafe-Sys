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

export interface OrderDetail {
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

export interface NuevoProducto {
  name: string;
  description?: string;
  price: number;
  imageUrl?: string;
  category: number;
  status?: string;
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

  getOrderDetails(): Observable<OrderDetail[]> {
    return this.http.get<OrderDetail[]>(`${this.API_URL}/order-details/`).pipe(timeout(this.TIMEOUT));
  }
}
