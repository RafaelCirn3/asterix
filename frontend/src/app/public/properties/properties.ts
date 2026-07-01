import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { Property } from '../../core/models/property.model';
import { MOCK_PROPERTIES } from '../../core/services/mock-properties';
import { PropertyService } from '../../core/services/property.service';
import { PropertyCard } from '../../shared/components/property-card/property-card';

@Component({
  selector: 'app-properties',
  imports: [PropertyCard, ReactiveFormsModule, RouterLink],
  templateUrl: './properties.html',
  styleUrl: './properties.scss',
})
export class Properties implements OnInit {
  private readonly fb = inject(FormBuilder);
  readonly properties = signal<Property[]>([]);
  readonly total = signal(0);
  readonly filterForm = this.fb.nonNullable.group({
    cidade: [''],
    bairro: [''],
    tipo: [''],
    preco_min: [''],
    preco_max: [''],
  });

  constructor(
    private readonly route: ActivatedRoute,
    private readonly router: Router,
    private readonly propertyService: PropertyService,
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.filterForm.patchValue({
        cidade: params['cidade'] ?? '',
        bairro: params['bairro'] ?? '',
        tipo: params['tipo'] ?? '',
        preco_min: params['preco_min'] ?? '',
        preco_max: params['preco_max'] ?? '',
      });
      this.load();
    });
  }

  load(): void {
    const raw = this.filterForm.getRawValue();
    this.propertyService
      .list({
        cidade: raw.cidade,
        bairro: raw.bairro,
        tipo: raw.tipo,
        preco_min: raw.preco_min ? Number(raw.preco_min) : undefined,
        preco_max: raw.preco_max ? Number(raw.preco_max) : undefined,
        size: 12,
      })
      .pipe(catchError(() => of({ items: MOCK_PROPERTIES, total: MOCK_PROPERTIES.length, page: 1, size: 12 })))
      .subscribe((response) => {
        this.properties.set(response.items);
        this.total.set(response.total);
      });
  }

  applyFilters(): void {
    const values = this.filterForm.getRawValue();
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        cidade: values.cidade || null,
        bairro: values.bairro || null,
        tipo: values.tipo || null,
        preco_min: values.preco_min || null,
        preco_max: values.preco_max || null,
      },
    });
  }
}
