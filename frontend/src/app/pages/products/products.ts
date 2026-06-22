import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService, Categoria, Producto } from '../../services/api';

@Component({
  standalone: true,
  selector: 'app-products',
  imports: [FormsModule],
  templateUrl: './products.html',
  styleUrls: ['./products.css']
})
export class ProductsComponent implements OnInit {

  private apiService = inject(ApiService);

  // ── Datos ──────────────────────────────────────────────────────────────
  productos = signal<Producto[]>([]);
  categorias = signal<Categoria[]>([]);

  // ── Estado de la UI ────────────────────────────────────────────────────
  cargando = signal(false);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');

  // ── Modelo del formulario de creación ───────────────────────────────────
  nombre = signal('');
  descripcion = signal('');
  precio = signal<number | null>(null);
  imagenUrl = signal('');
  categoriaId = signal<number | null>(null);

  // ── Edición inline (fila que se está editando) ──────────────────────────
  editandoId = signal<number | null>(null);
  editNombre = signal('');
  editPrecio = signal<number | null>(null);
  editCategoriaId = signal<number | null>(null);
  editStatus = signal('active');
  guardandoEdicion = signal(false);

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando.set(true);

    // Cargamos categorías y productos en paralelo
    this.apiService.getCategories().subscribe({
      next: (data) => this.categorias.set(data),
      error: () => this.error.set('No se pudieron cargar las categorías.')
    });

    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.productos.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los productos.');
        this.cargando.set(false);
      }
    });
  }

  // ── CREAR ────────────────────────────────────────────────────────────────
  onSubmit() {
    // Validación básica en el frontend
    if (!this.nombre().trim()) {
      this.error.set('El nombre del producto es obligatorio.');
      return;
    }
    if (this.precio() === null || this.precio()! <= 0) {
      this.error.set('El precio debe ser mayor a 0.');
      return;
    }
    if (this.categoriaId() === null) {
      this.error.set('Debes seleccionar una categoría.');
      return;
    }

    this.error.set('');
    this.mensaje.set('');
    this.guardando.set(true);

    this.apiService.createProduct({
      name: this.nombre().trim(),
      description: this.descripcion().trim() || undefined,
      price: this.precio()!,
      imageUrl: this.imagenUrl().trim() || undefined,
      category: this.categoriaId()!
    }).subscribe({
      next: (nuevoProducto) => {
        this.productos.update(actuales => [...actuales, nuevoProducto]);
        this.mensaje.set(`✅ Producto "${nuevoProducto.name}" creado con éxito.`);
        this.guardando.set(false);
        this._limpiarFormulario();
      },
      error: (err) => {
        this.guardando.set(false);
        this.error.set(this._formatearErrorDjango(err));
      }
    });
  }

  private _limpiarFormulario() {
    this.nombre.set('');
    this.descripcion.set('');
    this.precio.set(null);
    this.imagenUrl.set('');
    this.categoriaId.set(null);
  }

  // ── EDITAR ───────────────────────────────────────────────────────────────
  iniciarEdicion(p: Producto) {
    this.error.set('');
    this.mensaje.set('');
    this.editandoId.set(p.id);
    this.editNombre.set(p.name);
    this.editPrecio.set(Number(p.price));
    this.editCategoriaId.set(p.category);
    this.editStatus.set(p.status);
  }

  cancelarEdicion() {
    this.editandoId.set(null);
  }

  guardarEdicion(p: Producto) {
    if (!this.editNombre().trim()) {
      this.error.set('El nombre del producto es obligatorio.');
      return;
    }
    if (this.editPrecio() === null || this.editPrecio()! <= 0) {
      this.error.set('El precio debe ser mayor a 0.');
      return;
    }

    this.error.set('');
    this.guardandoEdicion.set(true);

    this.apiService.updateProduct(p.id, {
      name: this.editNombre().trim(),
      price: this.editPrecio()!,
      category: this.editCategoriaId()!,
      status: this.editStatus()
    }).subscribe({
      next: (actualizado) => {
        // Reemplazamos el producto editado en la lista, sin recargar todo
        this.productos.update(actuales =>
          actuales.map(item => item.id === actualizado.id ? actualizado : item)
        );
        this.mensaje.set(`✅ Producto "${actualizado.name}" actualizado.`);
        this.guardandoEdicion.set(false);
        this.editandoId.set(null);
      },
      error: (err) => {
        this.guardandoEdicion.set(false);
        this.error.set(this._formatearErrorDjango(err));
      }
    });
  }

  // ── ELIMINAR ─────────────────────────────────────────────────────────────
  eliminarProducto(p: Producto) {
    const confirmado = confirm(`¿Eliminar "${p.name}"? Esta acción no se puede deshacer.`);
    if (!confirmado) return;

    this.error.set('');
    this.mensaje.set('');

    this.apiService.deleteProduct(p.id).subscribe({
      next: () => {
        this.productos.update(actuales => actuales.filter(item => item.id !== p.id));
        this.mensaje.set(`🗑️ Producto "${p.name}" eliminado.`);
      },
      error: () => {
        this.error.set(`No se pudo eliminar "${p.name}".`);
      }
    });
  }

  // ── Helper: extraer mensaje de error legible desde la respuesta de Django ──
  private _formatearErrorDjango(err: any): string {
    const detalle = err?.error;
    if (detalle && typeof detalle === 'object') {
      const primeraClave = Object.keys(detalle)[0];
      const primerError = Array.isArray(detalle[primeraClave])
        ? detalle[primeraClave][0]
        : detalle[primeraClave];
      return `${primeraClave}: ${primerError}`;
    }
    return 'Ocurrió un error. Intenta de nuevo.';
  }
}
