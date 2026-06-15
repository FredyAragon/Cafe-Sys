import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, catchError, switchMap } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Agregamos el token a la request saliente
    const reqConToken = this._agregarToken(req);

    return next.handle(reqConToken).pipe(
      catchError((error: HttpErrorResponse) => {

        // Si el servidor responde 401 (token expirado), intentamos refrescarlo una vez
        if (error.status === 401) {
          return this.authService.refreshAccessToken().pipe(
            switchMap(() => {
              // Reintentamos la request original con el nuevo token
              const reqReintentar = this._agregarToken(req);
              return next.handle(reqReintentar);
            }),
            catchError((errorRefresh) => {
              // Si el refresh también falla, cerramos sesión
              this.authService.logout();
              return throwError(() => errorRefresh);
            })
          );
        }

        return throwError(() => error);
      })
    );
  }

  private _agregarToken(req: HttpRequest<any>): HttpRequest<any> {
    const token = this.authService.getAccessToken();

    // Si no hay token (ej: la request de login), la dejamos pasar sin modificar
    if (!token) return req;

    return req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
}
