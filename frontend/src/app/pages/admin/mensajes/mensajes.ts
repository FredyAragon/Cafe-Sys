import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../services/api';

@Component({
  standalone: true,
  selector: 'app-mensajes',
  imports: [CommonModule],
  templateUrl: './mensajes.html',
  styleUrls: ['./mensajes.css']
})
export class MensajesComponent implements OnInit {
  private apiService = inject(ApiService);

  mensajes = signal<any[]>([]);
  mensajeSeleccionado = signal<any | null>(null);
  cargando = signal(true);
  error = signal('');

  ngOnInit() {
    this.cargarMensajes();
  }

  cargarMensajes() {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getMessages().subscribe({
      next: (data) => {
        this.mensajes.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los mensajes.');
        this.cargando.set(false);
      }
    });
  }

  seleccionarMensaje(msg: any) {
    this.mensajeSeleccionado.set(msg);
  }

  cerrarDetalle() {
    this.mensajeSeleccionado.set(null);
  }

  getNombreUsuario(msg: any): string {
    return msg.user?.firstName 
      ? `${msg.user.firstName} ${msg.user.lastName || ''}`.trim()
      : 'Anónimo';
  }

  getEmailUsuario(msg: any): string {
    return msg.user?.email || '';
  }

  formatearFecha(fecha: string): string {
    if (!fecha) return '';
    const d = new Date(fecha);
    return d.toLocaleDateString('es', {
      year: 'numeric', month: 'long', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  }

  marcarComoLeido(msg: any) {
    if (msg.isRead) return;
    this.apiService.updateMessage(msg.id, { isRead: true }).subscribe({
      next: () => {
        msg.isRead = true;
      },
      error: () => {}
    });
  }
}