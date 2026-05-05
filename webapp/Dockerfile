FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Como el contexto es ./webapp, el archivo ya está en la raíz del contexto
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copiamos todo lo que hay en el contexto (o sea, el contenido de webapp) a /app
COPY . .

EXPOSE 80
CMD ["python3", "-u", "server.py"]