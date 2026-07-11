# ☕ CafeSys — Frontend

<p align="center">
  <img src="https://img.shields.io/badge/Angular-21.1.4-DD0031?logo=angular&logoColor=white" alt="Angular 21.1.4" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Vitest-6E9F18?logo=vitest&logoColor=white" alt="Vitest" />
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Vercel-000000?logo=vercel&logoColor=white" alt="Vercel" />
</p>

Frontend de **CafeSys**, un sistema integral de gestión y tienda virtual diseñado para cafeterías. Desarrollado con [Angular CLI](https://github.com/angular/angular-cli) v21.1.4.

---

## 📂 Estructura del Proyecto

```
frontend/
├── public/                 # Archivos estáticos (favicon, imágenes, assets)
│   └── favicon.ico
├── src/
│   ├── app/
│   │   ├── guards/         # 🔒 Protección de rutas
│   │   │   ├── auth.guard.ts
│   │   │   └── role.guard.ts
│   │   ├── interceptors/   # 🔄 Interceptores HTTP
│   │   │   └── auth.interceptor.ts
│   │   ├── pages/          # 📄 Vistas y páginas de la aplicación
│   │   │   ├── admin/      # Panel de administración
│   │   │   │   ├── mensajes/
│   │   │   │   ├── ordenes/
│   │   │   │   └── users/
│   │   │   ├── cart/       # Carrito de compras
│   │   │   ├── categories/ # Catálogo de categorías
│   │   │   ├── contact/    # Formulario de contacto
│   │   │   ├── dashboard/  # Panel de control
│   │   │   ├── home/       # Página de inicio
│   │   │   ├── layouts/    # Estructuras comunes (Navbar, Sidebar)
│   │   │   ├── location/   # Ubicación de sucursales
│   │   │   ├── login/      # Autenticación
│   │   │   ├── menu/       # Carta / Menú
│   │   │   ├── products/   # Detalle y gestión de productos
│   │   │   └── register/   # Registro de usuarios
│   │   ├── services/       # 🔌 Servicios y lógica de negocio
│   │   │   ├── api-config.ts
│   │   │   ├── api.ts
│   │   │   ├── auth.service.ts
│   │   │   └── cart.service.ts
│   │   ├── app.config.ts   # Configuración global
│   │   ├── app.routes.ts   # Enrutamiento
│   │   └── app.ts          # Componente raíz
│   ├── index.html
│   ├── main.ts             # Punto de entrada
│   └── styles.css          # Estilos globales
├── angular.json
├── Dockerfile
├── package.json
├── tsconfig.json
└── vercel.json
```

---

## 🏗️ Arquitectura y Componentes Clave

| Módulo | Descripción |
|--------|-------------|
| **`guards/`** | Protegen el acceso a rutas. `auth.guard.ts` bloquea páginas privadas si el usuario no está autenticado; `role.guard.ts` restringe el acceso según el rol (Cliente vs. Administrador). |
| **`interceptors/`** | `auth.interceptor.ts` intercepta automáticamente las peticiones HTTP para inyectar el token JWT y gestionar errores globales del servidor. |
| **`services/`** | Capa de comunicación con el backend: `api.ts` maneja las peticiones, `auth.service.ts` controla la sesión y `cart.service.ts` gestiona el estado del carrito de compras. |
| **`pages/`** | Cada vista está aislada con sus archivos `.ts`, `.html` y `.css`, garantizando un diseño modular y mantenible. |

---

## 🚀 Comandos de Desarrollo

### Servidor de desarrollo

```bash
ng serve
```

La aplicación estará disponible en [`http://localhost:4200/`](http://localhost:4200/).  
Se recarga automáticamente al detectar cambios en los archivos fuente.

### Compilación para producción

```bash
ng build
```

Genera los archivos optimizados en el directorio `dist/`, listos para desplegar.

### Pruebas unitarias

```bash
ng test
```

Ejecuta el conjunto de pruebas con el framework **Vitest**.

---

## 🐳 Docker y Despliegue

| Entorno | Descripción |
|---------|-------------|
| **Local / Contenedor** | Incluye un `Dockerfile` optimizado para ejecutar la aplicación en contenedores, tanto en entornos locales como en la nube. |
| **Producción (Cloud)** | El archivo `vercel.json` permite el despliegue directo en [Vercel](https://vercel.com) con Integración Continua (CI/CD). |

---

## 🛠️ Generación de Código (Scaffolding)

Angular CLI proporciona herramientas de andamiaje para crear componentes y servicios rápidamente:

```bash
# Generar un nuevo componente
ng generate component nombre-del-componente

# Generar un nuevo servicio
ng generate service services/nombre-del-servicio
```

---

<p align="center">
  <sub>Desarrollado con ☕ y Angular</sub>
</p>
