import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { getApiUrl } from '../../../services/api-config';

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
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './users.html',
  styleUrls: ['./users.css']
})
export class UsersComponent implements OnInit {
  private http = inject(HttpClient);
  private fb = inject(FormBuilder);
  
  private readonly API_URL = `${getApiUrl()}/users/`;

  users: User[] = [];
  userForm: FormGroup;
  isEditing = false;
  currentUserId: number | null = null;

  constructor() {
    this.userForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      role: ['', Validators.required],
      is_staff: [false],
      password: [''] 
    });
  }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.http.get<User[]>(this.API_URL).subscribe({
      next: (data) => this.users = data,
      error: (err) => console.error('Error al cargar usuarios:', err)
    });
  }

  onSubmit(): void {
    if (!this.isEditing || !this.currentUserId) {
      alert('Seleccione un usuario existente para editar.');
      return;
    }

    if (this.userForm.invalid) return;

    const payload: any = {
      email: this.userForm.value.email,
      firstName: this.userForm.value.first_name,
      lastName: this.userForm.value.last_name,
      role: this.userForm.value.role,
      is_staff: this.userForm.value.is_staff,
    };

    if (this.userForm.value.password) {
      payload.password = this.userForm.value.password;
    }

    this.http.patch(`${this.API_URL}${this.currentUserId}/`, payload).subscribe({
      next: () => {
        this.loadUsers();
        this.resetForm();
      },
      error: (err) => console.error('Error al actualizar usuario:', err)
    });
  }

  editUser(user: User): void {
    this.isEditing = true;
    this.currentUserId = user.id;
    this.userForm.patchValue({
      email: user.email,
      first_name: user.firstName,
      last_name: user.lastName,
      role: user.role,
      is_staff: user.is_staff,
      password: '' // Se deja en blanco por seguridad
    });
  }

  deleteUser(id: number): void {
    if (confirm('¿Está seguro de eliminar este usuario? Esta acción es irreversible.')) {
      this.http.delete(`${this.API_URL}${id}/`).subscribe({
        next: () => this.loadUsers(),
        error: (err) => console.error('Error al eliminar usuario:', err)
      });
    }
  }

  resetForm(): void {
    this.isEditing = false;
    this.currentUserId = null;
    this.userForm.reset();
  }
}