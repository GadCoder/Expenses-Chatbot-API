# Usa una imagen oficial de Python como base
FROM python:3.12-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Crea y usa un directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias

# Instala dependencias (usa uno u otro)
# Opción 1: con pip (si usas requirements.txt)
# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install psycopg2-binary

COPY ./src ./src

# Opción 2: con poetry
# RUN pip install poetry && poetry install --no-root --only main

# Copia el resto del proyecto
COPY . .

# Expone el puerto de FastAPI (por defecto 8000)
EXPOSE 8000

ENV PYTHONPATH="/app/src"

# Comando para correr la app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
