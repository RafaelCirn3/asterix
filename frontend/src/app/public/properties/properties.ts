import {
  ChangeDetectionStrategy,
  Component,
  computed,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

interface Property {
  id: number;
  title: string;
  address: string;
  neighborhood: string;
  city: string;
  state: string;

  type: string;

  bedrooms: number;
  bathrooms: number;
  parkingSpaces: number;

  area: number;

  price: number;
  condominium?: number;
  iptu?: number;

  image: string;

  featured?: boolean;
}

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
  ],
  templateUrl: './search.html',
  styleUrl: './search.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Search {

  // ==========================================================
  // ESTADO
  // ==========================================================

  readonly currentPage = signal(1);

  readonly totalPages = signal(23);

  readonly visiblePages = signal(5);

  readonly pageWindow = computed(() => {

    const current = this.currentPage();
    const visible = this.visiblePages();
    const total = this.totalPages();

    const block = Math.floor((current - 1) / visible);

    const start = block * visible + 1;

    const end = Math.min(start + visible - 1, total);

    return Array.from(
      { length: end - start + 1 },
      (_, index) => start + index
    );

  });

  readonly showEllipsis = computed(() => {

    return this.pageWindow().at(-1)! < this.totalPages();

  });

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

  // ==========================================================
  // DADOS (Mock)
  // ==========================================================

  readonly properties = signal<Property[]>([
    {
      id: 1,
      title: 'Apartamento para alugar com 2 quartos',
      address: 'Rua Bom Pastor',
      neighborhood: 'Tijuca',
      city: 'Rio de Janeiro',
      state: 'RJ',
      type: 'Apartamento',
      bedrooms: 2,
      bathrooms: 2,
      parkingSpaces: 1,
      area: 89,
      price: 2500,
      condominium: 869,
      iptu: 156,
      image: 'assets/images/property-1.jpg',
      featured: true,
    },

    {
      id: 2,
      title: 'Apartamento para alugar com 3 quartos',
      address: 'Rua José Higino',
      neighborhood: 'Tijuca',
      city: 'Rio de Janeiro',
      state: 'RJ',
      type: 'Apartamento',
      bedrooms: 3,
      bathrooms: 3,
      parkingSpaces: 1,
      area: 110,
      price: 2800,
      condominium: 2061,
      iptu: 318,
      image: 'assets/images/property-2.jpg',
    },

    {
      id: 3,
      title: 'Cobertura para alugar',
      address: 'Rua Bom Pastor',
      neighborhood: 'Tijuca',
      city: 'Rio de Janeiro',
      state: 'RJ',
      type: 'Cobertura',
      bedrooms: 2,
      bathrooms: 3,
      parkingSpaces: 3,
      area: 168,
      price: 3600,
      condominium: 2100,
      iptu: 318,
      image: 'assets/images/property-3.jpg',
    },
  ]);

  // ==========================================================
  // PAGINAÇÃO
  // ==========================================================

  goToPage(page: number): void {

    if (page < 1 || page > this.totalPages()) {
      return;
    }

    this.currentPage.set(page);

  }

  nextPage(): void {

    if (this.currentPage() < this.totalPages()) {

      this.currentPage.update(value => value + 1);

    }

  }

  previousPage(): void {

    if (this.currentPage() > 1) {

      this.currentPage.update(value => value - 1);

    }

  }

  // ==========================================================
  // FILTROS
  // ==========================================================

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

    this.bedrooms.set(value);

  }

  selectBathrooms(value: number): void {

    this.bathrooms.set(value);

  }

  selectParkingSpaces(value: number): void {

    this.parkingSpaces.set(value);

  }

  clearFilters(): void {

    this.propertyTypes.set([]);

    this.bedrooms.set(null);

    this.bathrooms.set(null);

    this.parkingSpaces.set(null);

  }

  search(): void {

    console.log('Buscar imóveis');

    console.log({

      transaction: this.selectedTransaction(),

      propertyTypes: this.propertyTypes(),

      bedrooms: this.bedrooms(),

      bathrooms: this.bathrooms(),

      parkingSpaces: this.parkingSpaces(),

    });

  }

  // ==========================================================
  // UTILITÁRIOS
  // ==========================================================

  trackByProperty(_: number, property: Property): number {

    return property.id;

  }

}