import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { timeout } from 'rxjs';
import { getApiUrl } from '../../services/api-config';

export interface Categoria {
  id: number;
  name: string;
  description: string | null;
  imageUrl: string | null;
  status: string;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './categories.html',
  styleUrls: ['./categories.css']
})
export class CategoriesComponent implements OnInit {
  private http = inject(HttpClient);
  private fb = inject(FormBuilder);

  private readonly API_URL = `${getApiUrl()}/categories/`;

  categorias = signal<Categoria[]>([]);
  cargando = signal(false);
  error = signal('');
  showForm = signal(false);
  isEditing = signal(false);
  editingId = signal<number | null>(null);

  categoriaForm: FormGroup;

  constructor() {
    this.categoriaForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      status: ['active']
    });
  }

  ngOnInit(): void {
    this.cargarCategorias();
  }

  cargarCategorias(): void {
    this.cargando.set(true);
    this.error.set('');

    this.http.get<Categoria[]>(this.API_URL).pipe(timeout(8000)).subscribe({
      next: (data) => {
        this.categorias.set(data);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar categorias:', err);
        if (err.name === 'TimeoutError') {
          this.error.set('El servidor no respondio a tiempo. Verifica que el backend este corriendo.');
        } else {
          this.error.set('No se pudieron cargar las categorias. Verifica la conexion con el backend.');
        }
        this.cargando.set(false);
      }
    });
  }

  abrirFormulario(): void {
    this.showForm.set(true);
    this.isEditing.set(false);
    this.editingId.set(null);
    this.categoriaForm.reset({ name: '', description: '', status: 'active' });
  }

  cerrarFormulario(): void {
    this.showForm.set(false);
    this.isEditing.set(false);
    this.editingId.set(null);
    this.categoriaForm.reset({ name: '', description: '', status: 'active' });
  }

  onSubmit(): void {
    if (this.categoriaForm.invalid) return;

    const payload = {
      name: this.categoriaForm.value.name,
      description: this.categoriaForm.value.description || null,
      status: this.categoriaForm.value.status
    };

    if (this.isEditing() && this.editingId()) {
      // Editar
      this.http.patch(`${this.API_URL}${this.editingId()}/`, payload).pipe(timeout(8000)).subscribe({
        next: () => {
          this.cargarCategorias();
          this.cerrarFormulario();
        },
        error: (err) => {
          console.error('Error al actualizar categoria:', err);
          this.error.set('No se pudo actualizar la categoria.');
        }
      });
    } else {
      // Crear
      this.http.post(this.API_URL, payload).pipe(timeout(8000)).subscribe({
        next: () => {
          this.cargarCategorias();
          this.cerrarFormulario();
        },
        error: (err) => {
          console.error('Error al crear categoria:', err);
          this.error.set('No se pudo crear la categoria. Verifica que el nombre no exista.');
        }
      });
    }
  }

  editarCategoria(cat: Categoria): void {
    this.showForm.set(true);
    this.isEditing.set(true);
    this.editingId.set(cat.id);
    this.categoriaForm.patchValue({
      name: cat.name,
      description: cat.description || '',
      status: cat.status
    });
  }

  eliminarCategoria(id: number): void {
    if (!confirm('¿Esta seguro de eliminar esta categoria? Esta accion es irreversible.')) return;

    this.http.delete(`${this.API_URL}${id}/`).pipe(timeout(8000)).subscribe({
      next: () => this.cargarCategorias(),
      error: (err) => {
        console.error('Error al eliminar categoria:', err);
        this.error.set('No se pudo eliminar la categoria.');
      }
    });
  }
}
