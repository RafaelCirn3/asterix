export type PropertyStatus = 'Disponivel' | 'Vendido' | 'Alugado';
export type PropertyAdType = 'Aluguel' | 'Venda';

export interface PropertyImage {
  id: number;
  imovel_id: number;
  arquivo: string;
  principal: boolean;
  ordem: number;
  url?: string;
}

export interface Property {
  id: number;
  nome: string;
  descricao_curta: string | null;
  descricao: string | null;
  preco: number | null;
  cidade: string | null;
  bairro: string | null;
  endereco: string | null;
  tipo: string | null;
  tipo_anuncio: PropertyAdType | null;
  numero: string | null;
  area: number | null;
  quartos: number | null;
  banheiros: number | null;
  garagem: number | null;
  status: PropertyStatus;
  destacado: boolean;
  created_at: string;
  updated_at: string;
  imagens: PropertyImage[];
}

export type PropertyPayload = Omit<Property, 'id' | 'created_at' | 'updated_at' | 'imagens'>;

export interface PropertyList {
  items: Property[];
  total: number;
  page: number;
  size: number;
}

export interface PropertyFilters {
  cidade?: string;
  bairro?: string;
  tipo?: string;
  tipo_anuncio?: PropertyAdType;
  destacado?: boolean;
  preco_min?: number;
  preco_max?: number;
  search?: string;
  page?: number;
  size?: number;
}
