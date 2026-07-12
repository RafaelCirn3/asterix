import { CurrencyPipe } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Property } from '../../../core/models/property.model';
import { STATIC_URL } from '../../../core/services/api-url';

@Component({
  selector: 'app-property-card',
  standalone: true,
  imports: [CurrencyPipe, RouterLink],
  templateUrl: './property-card.html',
  styleUrls: ['./property-card.scss'],
})
export class PropertyCard {

  @Input({ required: true })
  property!: Property;

  get imageUrl(): string {
    const selected =
      this.property?.imagens?.find(item => item.principal) ??
      this.property?.imagens?.[0];

    return selected?.url
      ? `${STATIC_URL}${selected.url}`
      : 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80';
  }
}