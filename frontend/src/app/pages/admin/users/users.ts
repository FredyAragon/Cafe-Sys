import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, UserDetail } from '../../../services/api';

export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
  is_staff: boolean;
}

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './users.html',
  styleUrls: ['./users.css']
})
export class UsersComponent implements OnInit {
  private apiService = inject(ApiService);

  users: User[] = [];
  editingId: number | null = null;
  editData: Partial<User> = {};
  cargando = signal(true);
  error = signal('');

  // Sorting
  sortKey: keyof User = 'id';
  sortDir: 'asc' | 'desc' = 'asc';

  roles = ['Customer', 'Admin', 'Driver', 'Employee'];

  ngOnInit(): void {
    this.loadUsers();
  }

  sortUsers(key: keyof User): void {
    if (this.sortKey === key) {
      this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = key;
      this.sortDir = 'asc';
    }
    this.applySort();
  }

  private applySort(): void {
    const key = this.sortKey;
    const dir = this.sortDir;
    const isNumericSort = key === 'id' || key === 'is_staff';
    this.users = [...this.users].sort((a, b) => {
      const aVal = a[key];
      const bVal = b[key];
      if (isNumericSort) {
        const numA = Number(aVal as any) || 0;
        const numB = Number(bVal as any) || 0;
        return dir === 'asc' ? numA - numB : numB - numA;
      }
      const strA = (String(aVal ?? '')).toLowerCase();
      const strB = (String(bVal ?? '')).toLowerCase();
      if (strA < strB) return dir === 'asc' ? -1 : 1;
      if (strA > strB) return dir === 'asc' ? 1 : -1;
      return 0;
    });
  }

  loadUsers(): void {
    this.cargando.set(true);
    this.error.set('');

    this.apiService.getUsers().subscribe({
      next: (data: UserDetail[]) => {
        console.log('USUARIOS OK:', data);
        this.users = data.map(u => ({
          id: u.id,
          email: u.email,
          firstName: u.firstName,
          lastName: u.lastName,
          role: u.role,
          is_staff: u.is_staff
        }));
        this.cargando.set(false);
      },
      error: (err: any) => {
        console.error('Error al cargar usuarios:', err);
        this.error.set('No se pudieron cargar los usuarios. Verifica tu permiso de administrador.');
        this.cargando.set(false);
      }
    });
  }

  startEdit(user: User): void {
    this.editingId = user.id;
    this.editData = {
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
      role: user.role
    };
  }

  cancelEdit(): void {
    this.editingId = null;
    this.editData = {};
  }

  saveEdit(user: User): void {
    if (!this.editData.firstName || !this.editData.lastName || !this.editData.email) {
      return;
    }

    const payload: any = {
      firstName: this.editData.firstName,
      lastName: this.editData.lastName,
      email: this.editData.email,
      role: this.editData.role,
    };

    this.apiService.updateUser(user.id, payload).subscribe({
      next: () => {
        this.loadUsers();
        this.cancelEdit();
      },
      error: (err: any) => {
        console.error('Error al actualizar usuario:', err);
        alert('Error al actualizar el usuario.');
      }
    });
  }

  deleteUser(id: number): void {
    if (confirm('¿Está seguro de eliminar este usuario? Esta acción es irreversible.')) {
      this.apiService.deleteUser(id).subscribe({
        next: () => this.loadUsers(),
        error: (err: any) => console.error('Error al eliminar usuario:', err)
      });
    }
  }
}
