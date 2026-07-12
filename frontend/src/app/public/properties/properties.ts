import {
  ChangeDetectionStrategy,
  Component,
  computed,
  signal,
} from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PropertyCard } from '../../shared/components/property-card/property-card';
import { Property } from '../../core/models/property.model';



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
export class Properties {

  // ==========================================================
  // ESTADO
  // ==========================================================
  readonly total = computed(() => this.properties().length);

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
      nome: 'Apartamento na Tijuca',
      descricao_curta: 'Apartamento amplo e iluminado',
      descricao: '',
      preco: 2500,
      cidade: 'Rio de Janeiro',
      bairro: 'Tijuca',
      endereco: 'Rua Bom Pastor',
      tipo: 'Apartamento',
      area: 89,
      quartos: 2,
      banheiros: 2,
      garagem: 1,
      status: 'Disponivel',
      created_at: '',
      updated_at: '',
      imagens: []
    },
    {
      id: 2,
      nome: 'Apartamento com suíte',
      descricao_curta: 'Ótima localização',
      descricao: '',
      preco: 2800,
      cidade: 'Rio de Janeiro',
      bairro: 'Tijuca',
      endereco: 'Rua José Higino',
      tipo: 'Apartamento',
      area: 110,
      quartos: 3,
      banheiros: 3,
      garagem: 1,
      status: 'Disponivel',
      created_at: '',
      updated_at: '',
      imagens: []
    }
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