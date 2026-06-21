import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent {
  tarjetas = [
    { front: 'Nuestro Origen', back: 'Granos seleccionados de las mejores fincas para garantizar una taza perfecta.' },
    { front: 'El Ambiente', back: 'Un espacio diseñado bajo principios de armonía para que te relajes y disfrutes.' },
    { front: 'Sabor Único', back: 'Tueste artesanal que resalta las notas a chocolate, caramelo y frutos secos.' }
  ];
}