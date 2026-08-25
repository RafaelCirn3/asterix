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

  readonly featured = signal<Property[]>([]);

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
      .list({ size: 6, destacado: true })
      .pipe(
        catchError(() =>
          of({
            items: [],
            total: 0,
            page: 1,
            size: 6
          })
        )
      )
      .subscribe(response => {

        this.featured.set(response.items);

      });

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

  setTab(
    tab: 'comprar' | 'alugar'
  ): void {

    this.activeTab.set(tab);

  }

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
