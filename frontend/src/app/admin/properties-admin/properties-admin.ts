import { CurrencyPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { RouterLink } from '@angular/router';

import { Property } from '../../core/models/property.model';
import { AuthService } from '../../core/services/auth.service';
import { PropertyService } from '../../core/services/property.service';

@Component({
  selector: 'app-properties-admin',
  imports: [CurrencyPipe, MatButtonModule, MatIconModule, MatTableModule, ReactiveFormsModule, RouterLink],
  templateUrl: './properties-admin.html',
  styleUrl: './properties-admin.scss',
})
export class PropertiesAdmin implements OnInit {
  private readonly fb = inject(FormBuilder);
  readonly properties = signal<Property[]>([]);
  readonly displayedColumns = ['nome', 'localizacao', 'preco', 'status', 'acoes'];
  readonly form = this.fb.nonNullable.group({ search: [''] });

  constructor(
    private readonly service: PropertyService,
    readonly auth: AuthService,
  ) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.service
      .list({ search: this.form.value.search ?? '', size: 50 })
      .subscribe((response) => this.properties.set(response.items));
  }

  remove(property: Property): void {
    if (confirm(`Excluir ${property.nome}?`)) {
      this.service.remove(property.id).subscribe(() => this.load());
    }
  }
}
