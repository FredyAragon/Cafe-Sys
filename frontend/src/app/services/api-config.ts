/**
 * Configuration for the API base URL.
 * En desarrollo (localhost:4200) → apunta a 127.0.0.1:8081
 * En producción (Vercel)         → apunta a Render
 */

export function getApiBaseUrl(): string {
  if (typeof window === 'undefined') {
    return 'https://cafesys-backend.onrender.com';
  }
  const hostname = window.location.hostname;
  const isLocal =
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    hostname === '[::1]';

  if (isLocal) {
    return 'http://127.0.0.1:8081';
  }

  // Producción: apuntamos al backend desplegado en Render
  return 'https://cafesys-backend.onrender.com';
}

export const API_PREFIX = '/apps/core';

export function getApiUrl(): string {
  return `${getApiBaseUrl()}${API_PREFIX}`;
}