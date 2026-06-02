import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  
  // ¡CORREGIDO!: Usamos la ruta real dictada por tu archivo urls.py de Django
  private apiUrl = 'http://localhost:8081/apps/core/products/'; 

  // GET
  getDatos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  // POST
  postDatos(nuevoItem: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, nuevoItem);
  }
}