import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Categoria, Producto } from '../../services/api';
import { CartService } from '../../services/cart.service';

@Component({
  standalone: true,
  selector: 'app-menu',
  imports: [CommonModule],
  templateUrl: './menu.html',
  styleUrls: ['./menu.css']
})
export class MenuComponent implements OnInit {
  private apiService = inject(ApiService);
  private cartService = inject(CartService);

  productos = signal<Producto[]>([]);
  categorias = signal<Categoria[]>([]);
  filtroCategoria = signal<number | null>(null);
  cargando = signal(false);
  mensaje = signal('');
  error = signal('');

  /** Feedback por producto: "añadido" o null */
  feedbackId = signal<number | null>(null);

  /** Producto que se está viendo en detalle */
  detalleProducto = signal<Producto | null>(null);

  ngOnInit() {
    this.cargarDatos();
  }

  get filteredProductos() {
    const catId = this.filtroCategoria();
    if (!catId) return this.productos();
    return this.productos().filter(p => p.category === catId);
  }

  cargarDatos() {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getCategories().subscribe({
      next: (data) => this.categorias.set(data.filter(c => c.status === 'active')),
      error: () => this.error.set('No se pudieron cargar las categorías.')
    });

    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.productos.set(data.filter(p => p.status === 'active'));
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los productos.');
        this.cargando.set(false);
      }
    });
  }

  agregarAlCarrito(producto: Producto) {
    this.cartService.addProduct(producto, 1);
    this.feedbackId.set(producto.id);
    this.mensaje.set(`✅ "${producto.name}" añadido a la cesta`);
    setTimeout(() => {
      this.feedbackId.set(null);
      this.mensaje.set('');
    }, 2000);
  }

  abrirDetalle(producto: Producto) {
    this.detalleProducto.set(producto);
  }

  cerrarDetalle() {
    this.detalleProducto.set(null);
  }
}
