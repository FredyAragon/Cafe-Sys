export function getApiBaseUrl(): string {
  if (typeof window === 'undefined') {
    return 'http://127.0.0.1:8081';
  }
  const hostname = window.location.hostname;
  const isLocal =
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    hostname === '[::1]';

  // Si quieres que en local también use Render, quita este if o cámbialo.
  // Como me dijiste que apunte al de Render, devolvemos la de Render directo:
  return 'https://cafesys-backend.onrender.com';
}

export const API_PREFIX = '/apps/core';

export function getApiUrl(): string {
  return `${getApiBaseUrl()}${API_PREFIX}`;
}