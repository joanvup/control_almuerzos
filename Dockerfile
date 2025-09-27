# Usa una imagen oficial de Python 3.11 como base
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# === INICIO DE LA LÍNEA CORREGIDA Y MÁS ROBUSTA ===
# Instala las herramientas de construcción esenciales y las librerías de desarrollo de MariaDB.
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && pip install --no-cache-dir -r requirements.txt
# === FIN DE LA LÍNEA CORREGIDA ===

# Copia el resto del código de tu aplicación al contenedor
COPY . .

# Expone el puerto que Gunicorn usará dentro del contenedor
EXPOSE 5000

# El comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "run:app"]