import { Component, signal, inject, OnInit } from '@angular/core';
import { ApiService } from './services/api';
import { FormsModule } from '@angular/forms'; // Necesario si quieres usar inputs en el HTML más adelante

@Component({
  selector: 'app-root',
  imports: [FormsModule], 
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private apiService = inject(ApiService);

  protected readonly title = signal('frontend');
  
  // Cambiamos el signal para que guarde una lista de objetos o elementos
  protected readonly listaElementos = signal<any[]>([]);
  protected readonly mensajeEstado = signal('Cargando datos...');

  ngOnInit(): void {
    this.cargarElementos();
  }

  // Ejecuta el GET
  cargarElementos(): void {
    this.apiService.getDatos().subscribe({
      next: (data) => {
        this.listaElementos.set(data);
        this.mensajeEstado.set('Datos cargados con éxito.');
      },
      error: (err) => {
        this.mensajeEstado.set('Error al traer datos de Django. ¿El endpoint /api/ existe?');
        console.error(err);
      }
    });
  }

  // Ejecuta el POST al presionar un botón
  enviarDataDePrueba(): void {
  // NOTA: Ajusta estas llaves exactamente como se llamen en tu models.py de Django
  // Te dejo un ejemplo asumiendo campos típicos en inglés y su relación con categorías/inventario
  const objetoDePrueba = {
    name: 'Café Americano Especial',
    price: '4.50',
    description: 'Generado desde pruebas de integración en Angular',
    stock: 50,
    category: 17 // Si tu producto exige un ID de categoría existente, asegúrate de poner un ID válido aquí
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
      console.error('Detalle del error de validación:', err.error); // <--- Esto te dirá exactamente qué campo falta o está mal
    }
  });
}
}