import {
  Component,
  ElementRef,
  HostListener,
  OnInit,
  ViewChild,
  inject,
  signal,
  computed
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
import { MOCK_PROPERTIES } from '../../core/services/mock-properties';
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
  styleUrl: './home.scss'
})
export class Home implements OnInit {

  private readonly fb = inject(FormBuilder);

  readonly featured = signal<Property[]>(MOCK_PROPERTIES);

  // ============================================================
  // DRAWER
  // ============================================================

  readonly drawerOpen = signal(false);

  @ViewChild('drawer')
  drawer!: ElementRef<HTMLDivElement>;

  // ============================================================
  // OPERAÇÃO
  // ============================================================

  readonly activeTab = signal<'comprar' | 'alugar'>('comprar');

  // ============================================================
  // PREÇO
  // ============================================================

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

  // ============================================================
  // QUARTOS
  // ============================================================

  readonly bedroomOptions = [1, 2, 3, 4];

  readonly bedrooms = signal<number | null>(null);

  // ============================================================
  // FORM
  // ============================================================

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

  // ============================================================
  // INIT
  // ============================================================

  ngOnInit(): void {

    this.propertyService
      .list({ size: 6 })
      .pipe(
        catchError(() =>
          of({
            items: MOCK_PROPERTIES,
            total: 3,
            page: 1,
            size: 6
          })
        )
      )
      .subscribe(response => {

        this.featured.set(
          response.items.length
            ? response.items
            : MOCK_PROPERTIES
        );

      });

  }

  // ============================================================
  // DRAWER
  // ============================================================

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

  // ============================================================
  // FECHAR COM ESC
  // ============================================================

  @HostListener('document:keydown.escape')

  onEscape(): void {

    if (this.drawerOpen()) {

      this.closeDrawer();

    }

  }

  // ============================================================
  // OPERAÇÃO
  // ============================================================

  setTab(
    tab: 'comprar' | 'alugar'
  ): void {

    this.activeTab.set(tab);

  }

  // ============================================================
  // PREÇO
  // ============================================================

  updatePrice(
    event: Event
  ): void {

    const value = Number(

      (event.target as HTMLInputElement).value

    );

    this.price.set(value);

    this.searchForm.patchValue({

      preco_max: value

    });

  }

  // ============================================================
  // QUARTOS
  // ============================================================

  selectBedrooms(
    value: number
  ): void {

    if (this.bedrooms() === value) {

      this.bedrooms.set(null);

      this.searchForm.patchValue({

        quartos: ''

      });

      return;

    }

    this.bedrooms.set(value);

    this.searchForm.patchValue({

      quartos: value.toString()

    });

  }

  // ============================================================
  // PESQUISA
  // ============================================================

  search(): void {

    const values = this.searchForm.getRawValue();

    this.closeDrawer();

    this.router.navigate(
      ['/imoveis'],
      {
        queryParams: {

          operacao: this.activeTab(),

          cidade:
            values.cidade || null,

          bairro:
            values.bairro || null,

          tipo:
            values.tipo || null,

          preco_max:
            values.preco_max || null,

          quartos:
            values.quartos || null

        }
      }
    );

  }

}