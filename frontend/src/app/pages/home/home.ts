import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService, Producto } from '../../services/api';

@Component({
  standalone: true,
  selector: 'app-home',
  imports: [CommonModule, RouterLink],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent implements OnInit {
  private apiService = inject(ApiService);

  tarjetas = [
    { front: 'Nuestro Origen', back: 'Granos seleccionados de las mejores fincas para garantizar una taza perfecta.' },
    { front: 'El Ambiente', back: 'Un espacio diseñado bajo principios de armonía para que te relajes y disfrutes.' },
    { front: 'Sabor Único', back: 'Tueste artesanal que resalta las notas a chocolate, caramelo y frutos secos.' }
  ];

  promociones = signal<any[]>([]);
  productosDestacados = signal<Producto[]>([]);
  resenas = signal<any[]>([]);
  cargando = signal(true);

  ngOnInit() {
    this.cargarDatos();
  }

  private cargarDatos() {
    this.cargando.set(true);

    this.apiService.getPromotions().subscribe({
      next: (data) => {
        const activas = data.filter((p: any) => p.status?.toLowerCase() === 'active');
        this.promociones.set(activas);
      },
      error: () => {}
    });

    this.apiService.getProducts().subscribe({
      next: (data) => {
        const activos = data.filter(p => p.status?.toLowerCase() === 'active');
        const destacados = activos.sort(() => 0.5 - Math.random()).slice(0, 4);
        this.productosDestacados.set(destacados);
      },
      error: () => {}
    });

    this.apiService.getReviews().subscribe({
      next: (data) => {
        this.resenas.set(data.slice(0, 3));
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
      }
    });
  }
}