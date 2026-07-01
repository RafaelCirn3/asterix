export type PropertyStatus = 'Disponivel' | 'Vendido' | 'Alugado';

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
  descricao_curta: string;
  descricao: string;
  preco: number;
  cidade: string;
  bairro: string;
  endereco: string;
  tipo: string;
  area: number;
  quartos: number;
  banheiros: number;
  garagem: number;
  status: PropertyStatus;
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
  preco_min?: number;
  preco_max?: number;
  search?: string;
  page?: number;
  size?: number;
}

