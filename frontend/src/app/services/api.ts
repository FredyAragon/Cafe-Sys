import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private readonly API_URL = 'http://127.0.0.1:8000/apps/core';

  constructor(private http: HttpClient) {}

  // ── PRODUCTOS ─────────────────────────────────────────────────────────────
  getProducts(): Observable<Producto[]> {
    return this.http.get<Producto[]>(`${this.API_URL}/products/`);
  }

  createProduct(productData: NuevoProducto): Observable<Producto> {
    return this.http.post<Producto>(`${this.API_URL}/products/`, productData);
  }

  updateProduct(id: number, productData: Partial<NuevoProducto>): Observable<Producto> {
    return this.http.patch<Producto>(`${this.API_URL}/products/${id}/`, productData);
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/products/${id}/`);
  }

  // ── CATEGORÍAS ────────────────────────────────────────────────────────────
  getCategories(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.API_URL}/categories/`);
  }

  createCategory(categoryData: NuevaCategoria): Observable<Categoria> {
    return this.http.post<Categoria>(`${this.API_URL}/categories/`, categoryData);
  }

  updateCategory(id: number, categoryData: Partial<NuevaCategoria>): Observable<Categoria> {
    return this.http.patch<Categoria>(`${this.API_URL}/categories/${id}/`, categoryData);
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/categories/${id}/`);
  }

  // Aquí irán los demás endpoints (órdenes, usuarios, etc.)
}
