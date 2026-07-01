import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Property, PropertyFilters, PropertyImage, PropertyList, PropertyPayload } from '../models/property.model';
import { API_URL } from './api-url';

@Injectable({ providedIn: 'root' })
export class PropertyService {
  constructor(private readonly http: HttpClient) {}

  list(filters: PropertyFilters = {}) {
    let params = new HttpParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params = params.set(key, String(value));
      }
    });
    return this.http.get<PropertyList>(`${API_URL}/imoveis`, { params });
  }

  get(id: number) {
    return this.http.get<Property>(`${API_URL}/imoveis/${id}`);
  }

  create(payload: PropertyPayload) {
    return this.http.post<Property>(`${API_URL}/imoveis`, payload);
  }

  update(id: number, payload: Partial<PropertyPayload>) {
    return this.http.patch<Property>(`${API_URL}/imoveis/${id}`, payload);
  }

  remove(id: number) {
    return this.http.delete<void>(`${API_URL}/imoveis/${id}`);
  }

  uploadImages(propertyId: number, files: File[]) {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    return this.http.post<PropertyImage[]>(`${API_URL}/imoveis/${propertyId}/imagens`, formData);
  }

  updateImage(propertyId: number, imageId: number, payload: Partial<PropertyImage>) {
    return this.http.patch<PropertyImage>(`${API_URL}/imoveis/${propertyId}/imagens/${imageId}`, payload);
  }

  deleteImage(propertyId: number, imageId: number) {
    return this.http.delete<void>(`${API_URL}/imoveis/${propertyId}/imagens/${imageId}`);
  }
}

