import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ApiService, Order, Producto, Categoria, UserDetail } from '../../services/api';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private apiService = inject(ApiService);

  usuario = this.authService.usuario;

  // ── Señales reactivas ──────────────────────────────────────────────────
  totalVentasHoy = signal('S/ 0.00');
  ordenesPendientes = signal(0);
  productosActivos = signal(0);
  clientesRegistrados = signal(0);
  categoriasActivas = signal(0);
  totalOrdenes = signal(0);
  ordenesArchivadas = signal(0);
  repartidoresActivos = signal(0);
  entregasPendientes = signal(0);
  promocionesActivas = signal(0);
  resenasRecientes = signal(0);
  mensajesNoLeidos = signal(0);
  mensajesRecientes = signal<any[]>([]);

  /** Top 3 clientes con más pedidos (Clientes Estrella) */
  clientesEstrella = signal<{ id: number; nombre: string; pedidos: number; total: number }[]>([]);

  /**
   * Estados de orden que representan ingresos reales (dinero efectivamente
   * comprometido/recibido). Excluimos las que aún no se confirman ('pending')
   * y las que fueron canceladas, para no inflar las ventas.
   */
  private readonly estadosConVenta = new Set(['assigned', 'preparing', 'ready', 'delivered']);

  // ── Datos para gráficos ────────────────────────────────────────────────
  ordenesPorEstado = signal<{ estado: string; cantidad: number; color: string }[]>([]);
  ventasPorDia = signal<{ dia: string; total: number }[]>([]);
  productosPorCategoria = signal<{ categoria: string; cantidad: number }[]>([]);

  // ── Órdenes recientes para la tabla ────────────────────────────────────
  ordenesRecientes = signal<Order[]>([]);

  // ── Actividad reciente (timeline) ──────────────────────────────────────
  actividadReciente = signal<{ icono: string; texto: string; tiempo: string }[]>([]);

  // ── Fechas calculadas ──────────────────────────────────────────────────

  cargando = signal(true);
  error = signal('');

  ngOnInit() {
    this.recargar();
  }

  recargar() {
    this.cargarDashboard();
  }

  /** Para el tooltip del gráfico de estados */
  maxOrdenesEstado = computed(() => {
    const data = this.ordenesPorEstado();
    if (data.length === 0) return 1;
    return Math.max(...data.map(d => d.cantidad), 1);
  });

  /** Máximo valor de ventas en los últimos 7 días */
  maxVentasSemana = computed(() => {
    const data = this.ventasPorDia();
    if (data.length === 0) return 1;
    return Math.max(...data.map(v => v.total), 1);
  });

  // Exponemos Math para uso en la plantilla
  Math = Math;

  private cargarDashboard() {
    this.cargando.set(true);
    this.error.set('');

    forkJoin({
      productos: this.apiService.getProducts(),
      categorias: this.apiService.getCategories(),
      ordenes: this.apiService.getOrders(),
      usuarios: this.apiService.getUsers(),
      entregas: this.apiService.getDeliveries(),
      promociones: this.apiService.getPromotions(),
      resenas: this.apiService.getReviews(),
      mensajes: this.apiService.getMessages(),
    }).subscribe({
      next: (data) => {
        // ── Productos activos ──────────────────────────────────────
        const activos = data.productos.filter(p => p.status?.toLowerCase() === 'active');
        this.productosActivos.set(activos.length);

        // ── Categorías activas ─────────────────────────────────────
        const catActivas = data.categorias.filter(c => c.status?.toLowerCase() === 'active');
        this.categoriasActivas.set(catActivas.length);

        // ── Órdenes ────────────────────────────────────────────────
        const ordenes = data.ordenes;
        this.totalOrdenes.set(ordenes.length);
        const pendientes = ordenes.filter(o => o.orderStatus?.toLowerCase() === 'pending');
        this.ordenesPendientes.set(pendientes.length);
        const archivadas = ordenes.filter(o => o.status?.toLowerCase() === 'inactive');
        this.ordenesArchivadas.set(archivadas.length);

        // Ventas de hoy: suma el total de las órdenes creadas hoy cuyo
        // estado representa ingreso real (excluye 'pending' y 'cancelled')
        const ordenesHoy = ordenes.filter(o => {
          const creada = new Date(o.created);
          const hoy = new Date();
          return creada.getDate() === hoy.getDate() &&
                 creada.getMonth() === hoy.getMonth() &&
                 creada.getFullYear() === hoy.getFullYear();
        });
        const conVentaHoy = ordenesHoy.filter(o =>
          this.estadosConVenta.has(o.orderStatus?.toLowerCase() || '')
        );
        const total = conVentaHoy.reduce((sum, o) => sum + parseFloat(o.total || '0'), 0);
        this.totalVentasHoy.set(`S/ ${total.toFixed(2)}`);

        // ── Órdenes recientes (últimas 5) ──────────────────────────
        const recientes = [...ordenes]
          .sort((a, b) => new Date(b.created).getTime() - new Date(a.created).getTime())
          .slice(0, 5);
        this.ordenesRecientes.set(recientes);

        // ── Usuarios/clientes ──────────────────────────────────────
        const clientes = data.usuarios.filter(u => u.role === 'Cliente' || u.role === 'Customer');
        this.clientesRegistrados.set(clientes.length);

        // ── Repartidores: usuarios con rol 'Driver' ────────────────
        const drivers = data.usuarios.filter(u => u.role === 'Driver');
        this.repartidoresActivos.set(drivers.length);

        // ── CLIENTES ESTRELLA: top 3 clientes con más pedidos ──────
        const conteo = new Map<number, { nombre: string; pedidos: number; total: number }>();
        for (const o of ordenes) {
          const id = o.user;
          const nombre = `${o.user_detail?.firstName || ''} ${o.user_detail?.lastName || ''}`.trim() || 'Usuario';
          const monto = parseFloat(o.total || '0');
          const actual = conteo.get(id) ?? { nombre, pedidos: 0, total: 0 };
          actual.pedidos += 1;
          actual.total += monto;
          conteo.set(id, actual);
        }
        const top = [...conteo.entries()]
          .map(([id, v]) => ({ id, ...v }))
          .sort((a, b) => b.pedidos - a.pedidos || b.total - a.total)
          .slice(0, 3);
        this.clientesEstrella.set(top);

        // ── Entregas pendientes ────────────────────────────────────
        const pendientesEntrega = data.entregas.filter((e: any) => e.deliveryStatus?.toLowerCase() === 'pending');
        this.entregasPendientes.set(pendientesEntrega.length);

        // ── Promociones activas ────────────────────────────────────
        const promosActivas = data.promociones.filter((p: any) => p.status?.toLowerCase() === 'active');
        this.promocionesActivas.set(promosActivas.length);

        // ── Reseñas recientes ──────────────────────────────────────
        this.resenasRecientes.set(data.resenas.length);

        // ── Mensajes no leídos ─────────────────────────────────────
        const noLeidos = data.mensajes.filter((m: any) => m.isRead === false);
        this.mensajesNoLeidos.set(noLeidos.length);
        this.mensajesRecientes.set(data.mensajes.slice(0, 5));

        // ── GRÁFICO: Órdenes por estado ────────────────────────────
        const estados = ['pending', 'assigned', 'preparing', 'ready', 'delivered', 'cancelled'];
        const colores: Record<string, string> = {
          pending: '#E65100',
          assigned: '#7C3AED',
          preparing: '#1565C0',
          ready: '#0F766E',
          delivered: '#2E7D32',
          cancelled: '#C62828'
        };
        const labels: Record<string, string> = {
          pending: 'Pendientes',
          assigned: 'Asignadas',
          preparing: 'Preparando',
          ready: 'Listas',
          delivered: 'Completadas',
          cancelled: 'Canceladas'
        };
        const ordenesEstado = estados.map(est => ({
          estado: labels[est],
          cantidad: ordenes.filter(o => o.orderStatus?.toLowerCase() === est).length,
          color: colores[est]
        }));
        this.ordenesPorEstado.set(ordenesEstado);

        // ── GRÁFICO: Ventas por día (últimos 7 días) ───────────────
        const ventasSemana: { dia: string; total: number }[] = [];
        for (let i = 6; i >= 0; i--) {
          const fecha = new Date();
          fecha.setDate(fecha.getDate() - i);
          const fechaStr = fecha.toLocaleDateString('es', { weekday: 'short' });
          const ordenesDia = ordenes.filter(o => {
            const creada = new Date(o.created);
            return creada.getDate() === fecha.getDate() &&
                   creada.getMonth() === fecha.getMonth() &&
                   creada.getFullYear() === fecha.getFullYear() &&
                   this.estadosConVenta.has(o.orderStatus?.toLowerCase() || '');
          });
          const totalDia = ordenesDia.reduce((sum, o) => sum + parseFloat(o.total || '0'), 0);
          ventasSemana.push({ dia: fechaStr, total: totalDia });
        }
        this.ventasPorDia.set(ventasSemana);

        // ── GRÁFICO: Productos por categoría ───────────────────────
        const cats = data.categorias.filter(c => c.status?.toLowerCase() === 'active');
        const prodCats = cats.map(c => ({
          categoria: c.name,
          cantidad: activos.filter(p => p.category === c.id).length
        }));
        this.productosPorCategoria.set(prodCats);

        // ── TIMELINE: Actividad reciente ───────────────────────────
        const actividad: { icono: string; texto: string; tiempo: string }[] = [];

        // Actividad de órdenes
        const ordenesRecientesTimeline = [...ordenes]
          .sort((a, b) => new Date(b.created).getTime() - new Date(a.created).getTime())
          .slice(0, 3);
        ordenesRecientesTimeline.forEach(o => {
          const tiempoRel = this.tiempoRelativo(o.created);
          actividad.push({
            icono: '📋',
            texto: `Nueva orden #${o.id} de ${o.user_detail?.firstName || 'Usuario'} — S/ ${o.total}`,
            tiempo: tiempoRel
          });
        });

        // Actividad de reseñas
        const resenasRecientes = [...data.resenas]
          .sort((a: any, b: any) => new Date(b.created || 0).getTime() - new Date(a.created || 0).getTime())
          .slice(0, 2);
        resenasRecientes.forEach((r: any) => {
          actividad.push({
            icono: '⭐',
            texto: `Nueva reseña: "${r.comment?.slice(0, 60)}${r.comment?.length > 60 ? '...' : ''}"`,
            tiempo: this.tiempoRelativo(r.created)
          });
        });

        // Actividad de mensajes
        if (noLeidos.length > 0) {
          actividad.push({
            icono: '✉️',
            texto: `${noLeidos.length} mensaje(s) sin leer`,
            tiempo: 'Ahora'
          });
        }

        this.actividadReciente.set(actividad.slice(0, 6));
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar dashboard:', err);
        this.error.set('No se pudieron cargar los datos del dashboard. Verifica la conexión con la API.');
        this.cargando.set(false);
      }
    });
  }

  private tiempoRelativo(fechaStr: string): string {
    if (!fechaStr) return '';
    const fecha = new Date(fechaStr);
    const ahora = new Date();
    const diffMs = ahora.getTime() - fecha.getTime();
    const diffMin = Math.floor(diffMs / 60000);
    const diffHoras = Math.floor(diffMs / 3600000);
    const diffDias = Math.floor(diffMs / 86400000);

    if (diffMin < 1) return 'Ahora';
    if (diffMin < 60) return `Hace ${diffMin} min`;
    if (diffHoras < 24) return `Hace ${diffHoras}h`;
    if (diffDias < 7) return `Hace ${diffDias}d`;
    return fecha.toLocaleDateString('es');
  }
}