export function getApiBaseUrl(): string {
  // Al poner el prefijo aquí, proteges tus endpoints si tus servicios llaman a esta función directamente
  return 'https://cafesys-backend.onrender.com/apps/core';
}

export const API_PREFIX = '/apps/core';

export function getApiUrl(): string {
  // Evitamos duplicar el prefijo por si acaso
  return getApiBaseUrl();
}