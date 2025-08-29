from flask_sqlalchemy import SQLAlchemy  # Importa la extensión SQLAlchemy para Flask

db = SQLAlchemy()  # Crea la instancia de la base de datos

class InputData(db.Model):  # Define el modelo InputData para la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna ID, clave primaria, tipo entero
    input_value = db.Column(db.String(120), nullable=False)  # Columna para el valor de entrada, tipo string, no nulo
    output_value = db.Column(db.String(120), nullable=False)  # Columna para el valor de salida, tipo string, no nulo

class ScrapedData(db.Model):  # Modelo para guardar los datos extraídos del scraping
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    title = db.Column(db.String(255), nullable=True)  # Título de la página
    logo_text = db.Column(db.String(255), nullable=True)  # Texto alternativo del logo
    links = db.Column(db.Text, nullable=True)         # Enlaces, guardados como texto separado por comas o pipes
    categories = db.Column(db.Text, nullable=True)     # Categorías principales
    banners = db.Column(db.Text, nullable=True)        # Banners/carousel
    buttons = db.Column(db.Text, nullable=True)        # Botones destacados
    footer = db.Column(db.Text, nullable=True)         # Texto del footer