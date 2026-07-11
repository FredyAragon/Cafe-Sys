import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';

@Component({
  standalone: true,
  selector: 'app-contact',
  imports: [CommonModule, FormsModule],
  templateUrl: './contact.html',
  styleUrls: ['./contact.css']
})
export class ContactComponent {
  private apiService = inject(ApiService);

  contactoNombre = signal('');
  contactoEmail = signal('');
  contactoTema = signal('');
  contactoMensaje = signal('');
  enviando = signal(false);
  mensajeEnviado = signal(false);
  errorEnvio = signal('');

  enviarMensaje() {
    const nombre = this.contactoNombre().trim();
    const email = this.contactoEmail().trim();
    const tema = this.contactoTema().trim();
    const mensaje = this.contactoMensaje().trim();

    if (!nombre || !email || !mensaje) {
      this.errorEnvio.set('Por favor completa todos los campos obligatorios.');
      this.mensajeEnviado.set(false);
      return;
    }

    this.enviando.set(true);
    this.errorEnvio.set('');

    // El modelo Messages espera subject y body
    // Guardamos el nombre y email dentro del body para referencia
    const asunto = tema ? `[${tema}] - ${nombre}` : `Contacto de ${nombre}`;
    const cuerpo = `De: ${nombre} (${email})\n\n${mensaje}`;

    this.apiService.createMessage({ subject: asunto, body: cuerpo }).subscribe({
      next: () => {
        this.mensajeEnviado.set(true);
        this.enviando.set(false);
        this.errorEnvio.set('');
        this.contactoNombre.set('');
        this.contactoEmail.set('');
        this.contactoTema.set('');
        this.contactoMensaje.set('');
        setTimeout(() => this.mensajeEnviado.set(false), 5000);
      },
      error: () => {
        this.enviando.set(false);
        this.errorEnvio.set('No se pudo enviar el mensaje. Intenta de nuevo más tarde.');
      }
    });
  }
}