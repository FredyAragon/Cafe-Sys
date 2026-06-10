import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8081/apps/core/products/';

  constructor(private http: HttpClient) {}

  // 1. Tu función GET actual (que ya funciona)
  getProducts(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  // 2. Tu función POST (Aquí es donde agregamos el Token obligatorio)
  createProduct(productData: any): Observable<any> {
    // 💡 PASO CLAVE: Simulamos que ya tenemos el token guardado.
    // Para esta prueba rápida, puedes pegar directamente el Access Token de Admin que obtuvimos en Postman:
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxMDM2Njc3LCJpYXQiOjE3ODEwMzMwNzcsImp0aSI6IjM0Njk1MmJiNWZmYzQ4MWQ5NmFlZmQxZmYxZDhjOTNhIiwidXNlcl9pZCI6MX0.RfeWDEV8euis4xDMqHKrl_cYzNAtEytSv8tP-cHA2rI'; 

    // Creamos las cabeceras e inyectamos el pasaporte Bearer
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    // Enviamos el POST incluyendo las cabeceras seguras
    return this.http.post(this.apiUrl, productData, { headers });
  }
}