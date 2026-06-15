import { Component, OnInit, signal, inject } from '@angular/core';
import { ApiService } from '../../services/api';

// ✅ usuario/cerrarSesion ahora viven en LayoutComponent (barra superior compartida).
//    Este componente solo se encarga de su propio contenido.
@Component({
  standalone: true,
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {

  private apiService = inject(ApiService);

  mensajeEstado = signal('Cargando...');
  listaElementos = signal<any[]>([]);

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
      name: 'Café Intruso Pro 3',
      price: 15.50,
      category: 1
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
