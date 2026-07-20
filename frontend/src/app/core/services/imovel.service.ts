import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Property } from '../models/property.model';
import { API_URL } from './api-url'; // confirme se o export se chama API_URL no seu api-url.ts

export interface ImovelListResponse {
    items: Property[];
    total: number;
    page: number;
    size: number;
}

export interface ImovelFiltros {
    cidade?: string | null;
    bairro?: string | null;
    tipo?: string | null;
    preco_min?: number | null;
    preco_max?: number | null;
    search?: string | null;
}

@Injectable({ providedIn: 'root' })
export class ImovelService {
    constructor(private http: HttpClient) { }

    listar(page: number, size: number, filtros: ImovelFiltros = {}): Observable<ImovelListResponse> {
        let params = new HttpParams().set('page', page).set('size', size);

        Object.entries(filtros).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== '') {
                params = params.set(key, value);
            }
        });

        return this.http.get<ImovelListResponse>(`${API_URL}/imoveis`, { params });
    }
}