import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  imports: [
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    RouterLink,
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private readonly fb = inject(FormBuilder);
  readonly error = signal('');
  readonly form = this.fb.nonNullable.group({
    email: ['admin@asterix.com.br', [Validators.required, Validators.email]],
    senha: ['admin123', Validators.required],
  });

  constructor(
    private readonly auth: AuthService,
    private readonly router: Router,
  ) {}

  submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.auth.login(this.form.value.email ?? '', this.form.value.senha ?? '').subscribe({
      next: () => this.router.navigateByUrl('/admin/dashboard'),
      error: (error) => {
        const message =
          error.status === 401
            ? 'Email ou senha invalidos.'
            : 'Nao foi possivel conectar a API. Verifique se o backend esta rodando.';
        this.error.set(message);
      },
    });
  }
}
