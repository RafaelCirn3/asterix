import { CurrencyPipe } from '@angular/common';
import { Component, OnInit, computed, signal } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, of, switchMap } from 'rxjs';

import { Property } from '../../core/models/property.model';
import { MOCK_PROPERTIES } from '../../core/services/mock-properties';
import { PropertyService } from '../../core/services/property.service';
import { STATIC_URL } from '../../core/services/api-url';
import { PropertyCard } from '../../shared/components/property-card/property-card';

@Component({
  selector: 'app-property-detail',
  imports: [CurrencyPipe, PropertyCard, RouterLink],
  templateUrl: './property-detail.html',
  styleUrl: './property-detail.scss',
})
export class PropertyDetail implements OnInit {
  readonly property = signal<Property | null>(null);
  readonly related = signal<Property[]>(MOCK_PROPERTIES.slice(0, 2));
  readonly coverImage = computed(() => {
    const item = this.property();
    const image = item?.imagens?.find((img) => img.principal) ?? item?.imagens?.[0];
    return image?.url
      ? `${STATIC_URL}${image.url}`
      : 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=80';
  });
  readonly mapUrl = computed<SafeResourceUrl>(() => {
    const item = this.property();
    const query = item ? `${item.endereco} ${item.cidade}` : 'Joao Pessoa PB';
    return this.sanitizer.bypassSecurityTrustResourceUrl(
      `https://maps.google.com/maps?q=${encodeURIComponent(query)}&output=embed`,
    );
  });

  constructor(
    private readonly route: ActivatedRoute,
    private readonly propertyService: PropertyService,
    private readonly sanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        switchMap((params) =>
          this.propertyService.get(Number(params.get('id'))).pipe(catchError(() => of(MOCK_PROPERTIES[0]))),
        ),
      )
      .subscribe((property) => this.property.set(property));
  }

  whatsappLink(property: Property): string {
    const message = encodeURIComponent(`Ola, quero mais informacoes sobre o imovel ${property.nome}.`);
    return `https://wa.me/5583999999999?text=${message}`;
  }
}
