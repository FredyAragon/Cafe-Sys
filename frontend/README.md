Markdown
# CafeSys - Frontend ☕

Este es el repositorio del frontend para **CafeSys**, un sistema de gestión y tienda virtual para una cafetería. El proyecto ha sido desarrollado utilizando [Angular CLI](https://github.com/angular/angular-cli) versión 21.1.4.

---

## 📂 Estructura del Proyecto (Tree)

A continuación se detalla la estructura principal de directorios y archivos clave del frontend:

```text
frontend/
├── public/                 # Archivos estáticos públicos (imágenes, favicon, etc.)
│   └── favicon.ico
├── src/                    # Código fuente de la aplicación
│   ├── app/                # Lógica principal de Angular
│   │   ├── guards/         # Protectores de rutas (Control de acceso)
│   │   │   ├── auth.guard.ts
│   │   │   └── role.guard.ts
│   │   ├── interceptors/   # Interceptores HTTP (Inyección de tokens)
│   │   │   └── auth.interceptor.ts
│   │   ├── pages/          # Componentes de vistas/páginas de la app
│   │   │   ├── admin/      # Panel de administración (Mensajes, Órdenes, Usuarios)
│   │   │   │   ├── mensajes/
│   │   │   │   ├── ordenes/
│   │   │   │   └── users/
│   │   │   ├── cart/       # Gestión del carrito de compras
│   │   │   ├── categories/ # Catálogo de categorías
│   │   │   ├── contact/    # Formulario de contacto
│   │   │   ├── dashboard/  # Panel de control general
│   │   │   ├── home/       # Página de inicio
│   │   │   ├── layouts/    # Estructuras de diseño comunes (Navbar, Sidebar)
│   │   │   ├── location/   # Ubicación de las sucursales
│   │   │   ├── login/      # Autenticación de usuarios
│   │   │   ├── menu/       # Carta/Menú de la cafetería
│   │   │   ├── products/   # Detalle/Gestión de productos
│   │   │   └── register/   # Registro de nuevos usuarios
│   │   ├── services/       # Servicios de comunicación con la API y estados
│   │   │   ├── api-config.ts
│   │   │   ├── api.ts
│   │   │   ├── auth.service.ts
│   │   │   └── cart.service.ts
│   │   ├── app.config.ts   # Configuración global del core de la aplicación
│   │   ├── app.routes.ts   # Enrutamiento general del sistema
│   │   └── app.ts          # Componente raíz (Root Component)
│   ├── index.html          # Archivo HTML principal
│   ├── main.ts             # Punto de entrada de la aplicación
│   └── styles.css          # Estilos globales
├── angular.json            # Configuración de Angular CLI
├── Dockerfile              # Configuración de contenedorización
├── package.json            # Dependencias del proyecto y scripts
├── tsconfig.json           # Configuración de TypeScript
└── vercel.json             # Configuración para despliegue en Vercel

## Arquitectura y Componentes Clave

guards/: Se encargan de proteger las rutas del sistema. auth.guard.ts evita el ingreso a páginas protegidas si el usuario no está logueado, y role.guard.ts restringe accesos específicos según el tipo de rol (ej. Cliente vs Admin).

interceptors/: auth.interceptor.ts intercepta de manera automática las peticiones HTTP salientes para adjuntar el token de autenticación (JWT) y manejar errores globales del servidor.

services/: Proveen la conexión al backend a través de api.ts, manejan la sesión en auth.service.ts y gestionan el estado pragmático de las compras a través de cart.service.ts.

pages/: Cada módulo visual está aislado con sus respectivos archivos .ts, .html y .css, asegurando un orden óptimo en el diseño del sistema de ventas.

## Servidor de Desarrollo

Para iniciar un servidor de desarrollo local, ejecuta el siguiente comando en la raíz del proyecto:

Bash
ng serve
Una vez que el servidor esté corriendo, abre tu navegador y navega a http://localhost:4200/. La aplicación se recargará automáticamente cada vez que modifiques cualquiera de los archivos fuente.

## Construcción (Build)
Para compilar el proyecto de cara a producción, ejecuta:

Bash
ng build
Esto compilará los archivos de TypeScript y optimizará los recursos dentro del directorio dist/. El build de producción optimiza la aplicación de manera automática para maximizar la velocidad y rendimiento.

## Docker y Despliegue
Local / Contenedor: Este proyecto incluye un Dockerfile optimizado para desplegar la aplicación mediante contenedores de manera local o en la nube.

Producción cloud: El proyecto cuenta con un archivo vercel.json listo para integrarse directamente con plataformas como Vercel mediante Integración Continua (CI/CD).

## Pruebas Unitarias
Para ejecutar las pruebas unitarias utilizando el framework de pruebas Vitest, usa el comando:

Bash
ng test
## Generación de Código (Scaffolding)
Angular CLI incluye potentes herramientas de andamiaje. Para generar un nuevo componente o servicio, utiliza:

Bash
# Generar un componente nuevo
ng generate component nombre-del-componente

# Generar un nuevo servicio
ng generate service services/nombre-del-servicio