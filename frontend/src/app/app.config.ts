import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { jwtInterceptor } from './services/jwt.interceptor'; // 👈 Tu interceptor en services
export const appConfig: ApplicationConfig = {
  providers: [
    // Activamos el cliente HTTP y le inyectamos nuestro interceptor funcional
    provideHttpClient(withInterceptors([jwtInterceptor]))
  ]
};