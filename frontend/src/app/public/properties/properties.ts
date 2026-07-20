import {
  ChangeDetectionStrategy,
  Component,
  computed,
  signal,
  OnInit,
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { PropertyCard } from '../../shared/components/property-card/property-card';
import { Property } from '../../core/models/property.model';
import { ImovelService } from '../../core/services/imovel.service';

@Component({
  selector: 'app-properties',
  standalone: true,
  imports: [
    CommonModule,
    PropertyCard
  ],
  templateUrl: './properties.html',
  styleUrls: ['./properties.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Properties implements OnInit {

  constructor(private imovelService: ImovelService) { }

  ngOnInit(): void {
    this.buscar();
  }

  // ==========================================================
  // ESTADO
  // ==========================================================

  readonly properties = signal<Property[]>([]);

  readonly loading = signal(true);

  readonly total = signal(0);

  readonly size = signal(9); // mesmo default do backend (ver app/routes/imoveis.py)

  readonly currentPage = signal(1);

  readonly drawerOpen = signal(false);

  readonly totalPages = computed(() =>
    Math.ceil(this.total() / this.size()) || 0
  );

  readonly visiblePages = signal(5);

  readonly pageWindow = computed(() => {

    const current = this.currentPage();
    const visible = this.visiblePages();
    const total = this.totalPages();

    const block = Math.floor((current - 1) / visible);

    const start = block * visible + 1;

    const end = Math.min(start + visible - 1, total);

    return Array.from(
      { length: Math.max(end - start + 1, 0) },
      (_, index) => start + index
    );

  });

  readonly showEllipsis = computed(() => {

    return this.pageWindow().at(-1)! < this.totalPages();

  });

  openDrawer(): void {

    this.drawerOpen.set(true);

    document.body.style.overflow = 'hidden';

  }

  closeDrawer(): void {

    this.drawerOpen.set(false);

    document.body.style.overflow = '';

  }

  // ==========================================================
  // FILTROS
  // ==========================================================

  readonly selectedTransaction = signal<'Comprar' | 'Alugar' | 'Lançamentos'>(
    'Alugar'
  );

  readonly propertyTypes = signal<string[]>([
    'Apartamento',
  ]);

  readonly bedrooms = signal<number | null>(null);

  readonly bathrooms = signal<number | null>(null);

  readonly parkingSpaces = signal<number | null>(null);

  togglePropertyType(type: string): void {

    const selected = this.propertyTypes();

    if (selected.includes(type)) {

      this.propertyTypes.set(
        selected.filter(item => item !== type)
      );

      return;
    }

    this.propertyTypes.set([
      ...selected,
      type,
    ]);

  }

  selectBedrooms(value: number): void {

    this.bedrooms.update(current =>
      current === value ? null : value
    );

  }

  selectBathrooms(value: number): void {

    this.bathrooms.update(current =>
      current === value ? null : value
    );

  }

  selectParkingSpaces(value: number): void {

    this.parkingSpaces.update(current =>
      current === value ? null : value
    );

  }

  clearFilters(): void {

    this.propertyTypes.set([]);

    this.bedrooms.set(null);

    this.bathrooms.set(null);

    this.parkingSpaces.set(null);

  }

  search(): void {

    this.currentPage.set(1);

    this.buscar();

    if (this.drawerOpen()) {

      this.closeDrawer();

    }

  }

  // ==========================================================
  // BUSCA (API real)
  // ==========================================================

  private buscar(): void {

    this.loading.set(true);

    const tipo = this.propertyTypes()[0] ?? null; // backend aceita 1 tipo por vez; ajuste se quiser múltiplos

    this.imovelService.listar(this.currentPage(), this.size(), {
      tipo,
      // cidade/bairro/search/preco_min/preco_max: plugue aqui se/quando existirem inputs de texto no filtro
    }).subscribe({
      next: (res) => {
        this.properties.set(res.items);
        this.total.set(res.total);
        this.size.set(res.size);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });

  }

  // ==========================================================
  // PAGINAÇÃO
  // ==========================================================

  goToPage(page: number): void {

    if (page < 1 || page > this.totalPages()) {
      return;
    }

    this.currentPage.set(page);

    this.buscar();

  }

  nextPage(): void {

    if (this.currentPage() < this.totalPages()) {

      this.currentPage.update(value => value + 1);

      this.buscar();

    }

  }

  previousPage(): void {

    if (this.currentPage() > 1) {

      this.currentPage.update(value => value - 1);

      this.buscar();

    }

  }

  // ==========================================================
  // UTILITÁRIOS
  // ==========================================================

  trackByProperty(_: number, property: Property): number {

    return property.id;

  }

}