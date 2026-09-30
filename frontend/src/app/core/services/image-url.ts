import { STATIC_URL } from './api-url';

/** Monta a URL de uma imagem tanto no ambiente local quanto em produção. */
export function imageUrl(path: string | null | undefined, fallback: string): string {
  if (!path) {
    return fallback;
  }

  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  return `${STATIC_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
}
