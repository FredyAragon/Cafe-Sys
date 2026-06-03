import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from './services/api'; 

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
// 💡 AQUÍ: Cambia "AppComponent" por "App" para que coincida con main.ts
export class App implements OnInit {
  title = signal('frontend');
  mensajeEstado = signal('Cargando...');
  listaElementos = signal<any[]>([]);

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.listaElementos.set(data);
        this.mensajeEstado.set('Datos cargados con éxito.');
      },
      error: () => this.mensajeEstado.set('Error al cargar datos.')
    });
  }

  enviarDataDePrueba() {
    this.mensajeEstado.set('Enviando objeto de prueba...');

    const nuevoProducto = {
      name: "Café Intruso Pro 3",
      price: 15.50,
      category: 17
    };

    this.apiService.createProduct(nuevoProducto).subscribe({
      next: (response) => {
        console.log('¡Producto creado con éxito desde Angular!', response);
        this.mensajeEstado.set('¡Objeto creado con éxito en Django!');
        this.listaElementos.update(actuales => [...actuales, response]);
      },
      error: (err) => {
        console.error('Detalle del error de validación:', err.error);
        this.mensajeEstado.set('Error al enviar el POST a Django.');
      }
    });
  }
}