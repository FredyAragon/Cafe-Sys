# Usamos una versión ligera de Node.js
FROM node:22-alpine

# Creamos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias
COPY package*.json ./

# Instalamos las dependencias del proyecto
RUN npm install

# Copiamos el resto del código del frontend
COPY . .

# Exponemos el puerto en el que corre Angular (según tus logs, el 8082)
EXPOSE 8082

# Comando para arrancar Angular en modo desarrollo con recarga en vivo
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "8082", "--poll", "2000"]