import { CurrencyPipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { API_URL } from '../../core/services/api-url';

interface DashboardData {
  quantidade_imoveis: number;
  quantidade_acessos: number;
  ultimos_imoveis: { id: number; nome: string; cidade: string; preco: number }[];
}

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe, MatButtonModule, MatCardModule, MatIconModule, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  readonly data = signal<DashboardData>({
    quantidade_imoveis: 0,
    quantidade_acessos: 0,
    ultimos_imoveis: [],
  });

  constructor(
    private readonly http: HttpClient,
    readonly auth: AuthService,
  ) {}

  ngOnInit(): void {
    this.http.get<DashboardData>(`${API_URL}/dashboard`).subscribe((response) => this.data.set(response));
  }
}

