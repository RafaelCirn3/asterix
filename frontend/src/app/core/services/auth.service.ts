import { HttpClient } from '@angular/common/http';
import { Injectable, computed, signal } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';

import { LoginResponse, User } from '../models/user.model';
import { API_URL } from './api-url';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly tokenKey = 'asterix_token';
  private readonly userKey = 'asterix_user';
  private readonly currentUser = signal<User | null>(this.readUser());

  readonly user = computed(() => this.currentUser());
  readonly isAuthenticated = computed(() => Boolean(this.token));

  constructor(
    private readonly http: HttpClient,
    private readonly router: Router,
  ) {}

  get token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  login(email: string, senha: string) {
    return this.http.post<LoginResponse>(`${API_URL}/auth/login`, { email, senha }).pipe(
      tap((response) => {
        localStorage.setItem(this.tokenKey, response.access_token);
        localStorage.setItem(this.userKey, JSON.stringify(response.usuario));
        this.currentUser.set(response.usuario);
      }),
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.currentUser.set(null);
    this.router.navigateByUrl('/admin/login');
  }

  private readUser(): User | null {
    const raw = localStorage.getItem(this.userKey);
    return raw ? (JSON.parse(raw) as User) : null;
  }
}

