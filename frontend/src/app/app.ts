import { Component, signal, inject, OnInit } from '@angular/core';
import { ApiService } from './services/api';
import { FormsModule } from '@angular/forms'; 
import { LoginComponent } from './components/login/login.component';

@Component({
  selector: 'app-root',
  standalone: true, // Aseguramos que sea standalone
  imports: [FormsModule, LoginComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private apiService = inject(ApiService);

  protected readonly title = signal('frontend');
  protected readonly listaElementos = signal<any[]>([]);
  protected readonly mensajeEstado = signal('Esperando prueba de JWT...');

  ngOnInit(): void {
    // 🛑 COMENTAMOS ESTO TEMPORALMENTE
    // Para que no tumbe la aplicación intentando buscar datos sin estar logueado.
    // this.cargarElementos();
  }

  // Ejecuta el GET antiguo
  cargarElementos(): void {
    this.apiService.getDatos().subscribe({
      next: (data) => {
        this.listaElementos.set(data);
        this.mensajeEstado.set('Datos cargados con éxito.');
      },
      error: (err) => {
        this.mensajeEstado.set('Error al traer datos de Django.');
        console.error(err);
      }
    });
  }

  // Ejecuta el POST antiguo
  enviarDataDePrueba(): void {
    const objetoDePrueba = {
      name: 'Café Americano Especial',
      price: '4.50',
      description: 'Generado desde pruebas de integración en Angular',
      stock: 50,
      category: 17 
    };

    this.mensajeEstado.set('Enviando datos...');

    this.apiService.postDatos(objetoDePrueba).subscribe({
      next: (respuesta) => {
        this.mensajeEstado.set('¡Elemento guardado con éxito en Django!');
        console.log('Respuesta del servidor:', respuesta);
        this.cargarElementos(); 
      },
      error: (err) => {
        this.mensajeEstado.set('Error al enviar el POST a Django.');
        console.error('Detalle del error:', err.error);
      }
    });
  }
}