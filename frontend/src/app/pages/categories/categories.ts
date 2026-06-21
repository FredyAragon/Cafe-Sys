import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

// Interfaz para tipar nuestros datos
export interface Category {
  id: number;
  name: string;
  description: string;
  status: string;
}

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './categories.html',
  styleUrls: ['./categories.css']
})
export class CategoriesComponent {
  // Datos simulados temporales para ver la maqueta
  categorias: Category[] = [
    { id: 1, name: 'Cafés Calientes', description: 'Espressos, americanos, lattes', status: 'active' },
    { id: 2, name: 'Bebidas Frías', description: 'Frappés y tés helados', status: 'active' },
    { id: 3, name: 'Postres', description: 'Tortas, galletas y muffins', status: 'active' },
    { id: 4, name: 'Merchandising', description: 'Tazas y termos', status: 'inactive' }
  ];
}