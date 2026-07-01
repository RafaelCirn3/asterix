import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { Property } from '../../core/models/property.model';
import { MOCK_PROPERTIES } from '../../core/services/mock-properties';
import { PropertyService } from '../../core/services/property.service';
import { PropertyCard } from '../../shared/components/property-card/property-card';

@Component({
  selector: 'app-home',
  imports: [PropertyCard, ReactiveFormsModule, RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home implements OnInit {
  private readonly fb = inject(FormBuilder);
  readonly featured = signal<Property[]>(MOCK_PROPERTIES);
  readonly searchForm = this.fb.nonNullable.group({
    cidade: [''],
    bairro: [''],
    tipo: [''],
    preco_max: [''],
  });

  constructor(
    private readonly propertyService: PropertyService,
    private readonly router: Router,
  ) {}

  ngOnInit(): void {
    this.propertyService
      .list({ size: 6 })
      .pipe(catchError(() => of({ items: MOCK_PROPERTIES, total: 3, page: 1, size: 6 })))
      .subscribe((response) => this.featured.set(response.items.length ? response.items : MOCK_PROPERTIES));
  }

  search(): void {
    const values = this.searchForm.getRawValue();
    this.router.navigate(['/imoveis'], {
      queryParams: {
        cidade: values.cidade || null,
        bairro: values.bairro || null,
        tipo: values.tipo || null,
        preco_max: values.preco_max || null,
      },
    });
  }
}
