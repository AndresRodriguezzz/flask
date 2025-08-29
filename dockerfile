FROM python:3.11-slim 
# Usa una imagen ligera de Python 3.11

WORKDIR /app  
# Establece el directorio de trabajo dentro del contenedor

COPY . /app 
 # Copia todos los archivos del proyecto al contenedor

# Instala las dependencias del proyecto desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 
 # Expone el puerto 8000 para la API Flask

CMD ["python", "app.py"]  
# Comando para iniciar la