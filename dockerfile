FROM python:3.11-slim  # Usa una imagen ligera de Python 3.11
WORKDIR /app  # Establece el directorio de trabajo
COPY . /app  # Copia todos los archivos al contenedor
RUN pip install --no-cache-dir -r requirements.txt  # Instala las dependencias
EXPOSE 8000  # Expone el puerto 8000 para la API
CMD ["python", "app.py"]  # Comando para iniciar la aplicación Flask