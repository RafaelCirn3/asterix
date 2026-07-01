import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { API_URL } from './api-url';

export interface ContactPayload {
  nome: string;
  email: string;
  telefone: string;
  mensagem: string;
}

@Injectable({ providedIn: 'root' })
export class ContactService {
  constructor(private readonly http: HttpClient) {}

  send(payload: ContactPayload) {
    return this.http.post(`${API_URL}/contato`, payload);
  }
}

