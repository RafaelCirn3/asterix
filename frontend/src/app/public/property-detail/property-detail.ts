import { CurrencyPipe } from '@angular/common';
import { Component, HostListener, OnInit, computed, signal } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, of, switchMap } from 'rxjs';

import { Property, PropertyImage } from '../../core/models/property.model';
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
  private readonly defaultWhatsappNumber = '556181200528';
  private readonly fallbackImage =
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=80';

  readonly property = signal<Property | null>(null);
  readonly related = signal<Property[]>([]);
  readonly selectedImageIndex = signal(0);
  readonly lightboxOpen = signal(false);

  readonly galleryImages = computed(() => {
    const images = this.property()?.imagens ?? [];
    const principal = images.find((image) => image.principal);
    return principal ? [principal, ...images.filter((image) => image.id !== principal.id)] : images;
  });

  readonly selectedImage = computed(() => this.galleryImages()[this.selectedImageIndex()]);
  readonly coverImage = computed(() => this.imageUrl(this.selectedImage()));

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
          this.propertyService
            .get(Number(params.get('id')))
            .pipe(catchError(() => of(null))),
        ),
      )
      .subscribe((property) => {
        this.lightboxOpen.set(false);
        this.selectedImageIndex.set(0);
        this.property.set(property);
      });
  }

  imageUrl(image?: PropertyImage): string {
    if (!image?.url) {
      return this.fallbackImage;
    }
    if (/^https?:\/\//i.test(image.url)) {
      return image.url;
    }
    return `${STATIC_URL.replace(/\/$/, '')}/${image.url.replace(/^\//, '')}`;
  }

  selectImage(index: number): void {
    if (index >= 0 && index < this.galleryImages().length) {
      this.selectedImageIndex.set(index);
    }
  }

  moveImage(direction: number): void {
    const length = this.galleryImages().length;
    if (length > 0) {
      this.selectedImageIndex.update((index) => (index + direction + length) % length);
    }
  }

  openLightbox(index = this.selectedImageIndex()): void {
    if (this.galleryImages().length > 0) {
      this.selectImage(index);
      this.lightboxOpen.set(true);
    }
  }

  closeLightbox(): void {
    this.lightboxOpen.set(false);
  }

  @HostListener('document:keydown', ['$event'])
  onKeydown(event: KeyboardEvent): void {
    if (!this.lightboxOpen()) {
      return;
    }
    if (event.key === 'Escape') {
      this.closeLightbox();
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      this.moveImage(1);
    } else if (event.key === 'ArrowLeft') {
      event.preventDefault();
      this.moveImage(-1);
    }
  }

  whatsappLink(property: Property): string {
    const number = this.normalizeWhatsappNumber(property.numero) || this.defaultWhatsappNumber;
    const anuncio = property.tipo_anuncio ? ` para ${property.tipo_anuncio.toLowerCase()}` : '';
    const message = encodeURIComponent(
      `Olá, quero mais informações sobre o imóvel ${property.nome}${anuncio}.`,
    );
    return `https://wa.me/${number}?text=${message}`;
  }

  private normalizeWhatsappNumber(value: string | null): string | null {
    const digits = value?.replace(/\D/g, '') ?? '';
    if (!digits) {
      return null;
    }

    if (digits.startsWith('55')) {
      return digits;
    }

    if (digits.length === 10 || digits.length === 11) {
      return `55${digits}`;
    }

    return digits;
  }
}
