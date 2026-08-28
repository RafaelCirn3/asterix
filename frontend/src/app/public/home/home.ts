import {
  Component,
  ElementRef,
  HostListener,
  OnInit,
  ViewChild,
  computed,
  inject,
  signal
} from '@angular/core';

import {
  FormBuilder,
  ReactiveFormsModule
} from '@angular/forms';

import {
  Router,
  RouterLink
} from '@angular/router';

import {
  catchError,
  of
} from 'rxjs';

import { Property } from '../../core/models/property.model';
import { PropertyService } from '../../core/services/property.service';
import { PropertyCard } from '../../shared/components/property-card/property-card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    PropertyCard,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './home.html',
  styleUrls: ['./home.scss', './home-carousel.scss', './home-searchbar-fix.scss']
})
export class Home implements OnInit {
  private readonly fb = inject(FormBuilder);

  readonly featured = signal<Property[]>([]);
  readonly featuredIndex = signal(0);
  readonly drawerOpen = signal(false);

  @ViewChild('drawer')
  drawer!: ElementRef<HTMLDivElement>;

  readonly activeTab = signal<'comprar' | 'alugar'>('comprar');
  readonly price = signal(800000);

  readonly priceLabel = computed(() =>
    this.price().toLocaleString(
      'pt-BR',
      {
        style: 'currency',
        currency: 'BRL',
        maximumFractionDigits: 0
      }
    )
  );

  readonly bedroomOptions = [1, 2, 3, 4];
  readonly bedrooms = signal<number | null>(null);

  readonly searchForm = this.fb.nonNullable.group({
    cidade: [''],
    bairro: [''],
    tipo: [''],
    preco_max: [this.price()],
    quartos: ['']
  });

  constructor(
    private readonly propertyService: PropertyService,
    private readonly router: Router
  ) { }

  ngOnInit(): void {
    this.propertyService
      .list({ size: 9, destacado: true })
      .pipe(
        catchError(() =>
          of({
            items: [],
            total: 0,
            page: 1,
            size: 9
          })
        )
      )
      .subscribe(response => {
        this.featured.set(response.items);
        this.featuredIndex.set(response.items.length > 1 ? 1 : 0);
      });
  }

  carouselClass(index: number): 'active' | 'previous' | 'next' | 'hidden' {
    const items = this.featured();
    const length = items.length;

    if (!length) {
      return 'hidden';
    }

    const active = this.featuredIndex();
    if (index === active) {
      return 'active';
    }

    const previous = (active - 1 + length) % length;
    const next = (active + 1) % length;

    if (index === previous) {
      return 'previous';
    }

    if (index === next) {
      return 'next';
    }

    return 'hidden';
  }

  previousFeatured(): void {
    const length = this.featured().length;
    if (length < 2) {
      return;
    }

    this.featuredIndex.update(index => (index - 1 + length) % length);
  }

  nextFeatured(): void {
    const length = this.featured().length;
    if (length < 2) {
      return;
    }

    this.featuredIndex.update(index => (index + 1) % length);
  }

  focusFeatured(index: number): void {
    if (index !== this.featuredIndex()) {
      this.featuredIndex.set(index);
    }
  }

  openDrawer(): void {
    this.drawerOpen.set(true);
    document.body.style.overflow = 'hidden';

    queueMicrotask(() => {
      this.drawer?.nativeElement
        ?.querySelector<HTMLInputElement>('input')
        ?.focus();
    });
  }

  closeDrawer(): void {
    this.drawerOpen.set(false);
    document.body.style.overflow = '';
  }

  toggleDrawer(): void {
    this.drawerOpen()
      ? this.closeDrawer()
      : this.openDrawer();
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    if (this.drawerOpen()) {
      this.closeDrawer();
    }
  }

  setTab(tab: 'comprar' | 'alugar'): void {
    this.activeTab.set(tab);
  }

  updatePrice(event: Event): void {
    const value = Number((event.target as HTMLInputElement).value);
    this.price.set(value);
    this.searchForm.patchValue({ preco_max: value });
  }

  selectBedrooms(value: number): void {
    if (this.bedrooms() === value) {
      this.bedrooms.set(null);
      this.searchForm.patchValue({ quartos: '' });
      return;
    }

    this.bedrooms.set(value);
    this.searchForm.patchValue({ quartos: value.toString() });
  }

  search(): void {
    const values = this.searchForm.getRawValue();
    this.closeDrawer();

    this.router.navigate(
      ['/imoveis'],
      {
        queryParams: {
          operacao: this.activeTab(),
          cidade: values.cidade || null,
          bairro: values.bairro || null,
          tipo: values.tipo || null,
          preco_max: values.preco_max || null,
          quartos: values.quartos || null
        }
      }
    );
  }
}
