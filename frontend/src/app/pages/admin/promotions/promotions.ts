import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../services/api';

export interface AdminPromotion {
  id: number;
  name: string;
  description: string | null;
  discount: string;
  discountType: 'percentage' | 'fixed';
  imageUrl: string | null;
  startDate: string;
  endDate: string;
  status: 'active' | 'inactive';
}

@Component({
  selector: 'app-admin-promotions',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './promotions.html',
  styleUrls: ['./promotions.css']
})
export class AdminPromotionsComponent implements OnInit {
  private apiService = inject(ApiService);

  promotions = signal<AdminPromotion[]>([]);
  cargando = signal(false);
  error = signal('');

  form = signal<Partial<AdminPromotion>>({
    name: '',
    description: '',
    discountType: 'percentage',
    status: 'active'
  });
  editId: number | null = null;
  mostrandoForm = signal(false);
  guardando = signal(false);

  ngOnInit(): void {
    this.loadPromotions();
  }

  loadPromotions(): void {
    this.cargando.set(true);
    this.error.set('');
    this.apiService.getPromotions().subscribe({
      next: (data: any[]) => {
        this.promotions.set(data.map(p => ({
          id: p.id,
          name: p.name,
          description: p.description ?? null,
          discount: typeof p.discount === 'number' ? p.discount : parseFloat(p.discount as any),
          discountType: p.discountType as AdminPromotion['discountType'],
          imageUrl: p.imageUrl ?? null,
          startDate: p.startDate,
          endDate: p.endDate,
          status: p.status as AdminPromotion['status']
        })));
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar promociones:', err);
        this.error.set('No se pudieron cargar las promociones.');
        this.cargando.set(false);
      }
    });
  }

  nuevo(): void {
    this.editId = null;
    this.mostrandoForm.set(true);
    this.form.set({
      name: '',
      description: '',
      discountType: 'percentage',
      status: 'active'
    });
  }

  editar(p: AdminPromotion): void {
    this.editId = p.id;
    this.mostrandoForm.set(true);
    this.form.set({ ...p });
  }

  cancelar(): void {
    this.editId = null;
    this.mostrandoForm.set(false);
    this.form.set({
      name: '',
      description: '',
      discountType: 'percentage',
      status: 'active'
    });
  }

  /** Actualiza un campo del formulario de forma reactiva (compatible con ngModel). */
  actualizarCampo(campo: keyof AdminPromotion, valor: any): void {
    this.form.update((f: Partial<AdminPromotion>) => ({ ...f, [campo]: valor }));
  }

  guardar(): void {
    if (!this.form().name || this.form().discount == null) return;

    this.guardando.set(true);
    this.error.set('');

    const today = new Date();
    const nextYear = new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());
    const toISO = (d: Date) => d.toISOString().slice(0, 10);

    const payload: any = {
      name: this.form().name,
      description: this.form().description ?? '',
      discountType: this.form().discountType || 'percentage',
      status: this.form().status || 'active',
      startDate: this.form().startDate || toISO(today),
      endDate: this.form().endDate || toISO(nextYear)
    };

    if (this.form().imageUrl) payload.imageUrl = this.form().imageUrl;

    if (this.editId) {
      payload.discount = Number(this.form().discount) || 0;
      this.apiService.updatePromotion(this.editId, payload).subscribe({
        next: () => { this.guardando.set(false); this.mostrandoForm.set(false); this.cancelar(); this.loadPromotions(); },
        error: (err: any) => { this.guardando.set(false); this.error.set('Error al actualizar promoción.'); console.error(err); }
      });
    } else {
      payload.discount = Number(this.form().discount) || 0;
      this.apiService.createPromotion(payload).subscribe({
        next: () => { this.guardando.set(false); this.mostrandoForm.set(false); this.cancelar(); this.loadPromotions(); },
        error: (err: any) => { this.guardando.set(false); this.error.set('Error al crear promoción.'); console.error(err); }
      });
    }
  }

  eliminar(p: AdminPromotion): void {
    if (!confirm(`Eliminar promoción "${p.name}"?`)) return;
    this.apiService.deletePromotion(p.id).subscribe({
      next: () => this.loadPromotions(),
      error: (err: any) => { this.error.set('No se pudo eliminar.'); console.error(err); }
    });
  }
}