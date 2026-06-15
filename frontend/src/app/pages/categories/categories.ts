import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService, Categoria } from '../../services/api';

@Component({
  standalone: true,
  selector: 'app-categories',
  imports: [FormsModule],
  templateUrl: './categories.html',
  styleUrls: ['./categories.css']
})
export class CategoriesComponent implements OnInit {

  private apiService = inject(ApiService);

  // ── Datos ──────────────────────────────────────────────────────────────
  categorias = signal<Categoria[]>([]);

  // ── Estado de la UI ────────────────────────────────────────────────────
  cargando = signal(false);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');

  // ── Modelo del formulario de creación ───────────────────────────────────
  nombre = signal('');
  descripcion = signal('');
  imagenUrl = signal('');

  // ── Edición inline (fila que se está editando) ──────────────────────────
  editandoId = signal<number | null>(null);
  editNombre = signal('');
  editDescripcion = signal('');
  editImagenUrl = signal('');
  editStatus = signal('active');
  guardandoEdicion = signal(false);

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando.set(true);

    this.apiService.getCategories().subscribe({
      next: (data) => {
        this.categorias.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar las categorías.');
        this.cargando.set(false);
      }
    });
  }

  // ── CREAR ────────────────────────────────────────────────────────────────
  onSubmit() {
    if (!this.nombre().trim()) {
      this.error.set('El nombre de la categoría es obligatorio.');
      return;
    }

    this.error.set('');
    this.mensaje.set('');
    this.guardando.set(true);

    this.apiService.createCategory({
      name: this.nombre().trim(),
      description: this.descripcion().trim() || undefined,
      imageUrl: this.imagenUrl().trim() || undefined
    }).subscribe({
      next: (nuevaCategoria) => {
        this.categorias.update(actuales => [...actuales, nuevaCategoria]);
        this.mensaje.set(`✅ Categoría "${nuevaCategoria.name}" creada con éxito.`);
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
    this.imagenUrl.set('');
  }

  // ── EDITAR ───────────────────────────────────────────────────────────────
  iniciarEdicion(c: Categoria) {
    this.error.set('');
    this.mensaje.set('');
    this.editandoId.set(c.id);
    this.editNombre.set(c.name);
    this.editDescripcion.set(c.description ?? '');
    this.editImagenUrl.set(c.imageUrl ?? '');
    this.editStatus.set(c.status);
  }

  cancelarEdicion() {
    this.editandoId.set(null);
  }

  guardarEdicion(c: Categoria) {
    if (!this.editNombre().trim()) {
      this.error.set('El nombre de la categoría es obligatorio.');
      return;
    }

    this.error.set('');
    this.guardandoEdicion.set(true);

    this.apiService.updateCategory(c.id, {
      name: this.editNombre().trim(),
      description: this.editDescripcion().trim() || undefined,
      imageUrl: this.editImagenUrl().trim() || undefined,
      status: this.editStatus()
    }).subscribe({
      next: (actualizada) => {
        this.categorias.update(actuales =>
          actuales.map(item => item.id === actualizada.id ? actualizada : item)
        );
        this.mensaje.set(`✅ Categoría "${actualizada.name}" actualizada.`);
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
  eliminarCategoria(c: Categoria) {
    const confirmado = confirm(`¿Eliminar "${c.name}"? Esta acción no se puede deshacer.`);
    if (!confirmado) return;

    this.error.set('');
    this.mensaje.set('');

    this.apiService.deleteCategory(c.id).subscribe({
      next: () => {
        this.categorias.update(actuales => actuales.filter(item => item.id !== c.id));
        this.mensaje.set(`🗑️ Categoría "${c.name}" eliminada.`);
      },
      error: (err) => {
        // ⚠️ Si la categoría tiene productos asociados, Django no permite borrarla
        //    (la relación Producto → Categoría es PROTECT). Mostramos un mensaje claro.
        if (err.status === 500 || err.status === 409 || err.status === 400) {
          this.error.set(`No se pudo eliminar "${c.name}": probablemente tiene productos asociados.`);
        } else {
          this.error.set(`No se pudo eliminar "${c.name}".`);
        }
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
