export interface User {
  id: number;
  nome: string;
  email: string;
  ativo: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: User;
}

