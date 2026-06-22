import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// ✅ El componente raíz ahora es minimalista: solo aloja el router.
//    Toda la lógica de productos/POST se movió a DashboardComponent (paso 4).
@Component({
  standalone: true,
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {}
