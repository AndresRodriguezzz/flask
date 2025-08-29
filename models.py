from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_value = db.Column(db.String(120), nullable=False)
    output_value = db.Column(db.String(120), nullable=False)

class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    logo_text = db.Column(db.String(255), nullable=True)
    links = db.Column(db.Text, nullable=True)         # Guarda como texto separado por comas
    categories = db.Column(db.Text, nullable=True)     # Guarda como texto separado por comas
    banners = db.Column(db.Text, nullable=True)        # Guarda como texto separado por comas
    buttons = db.Column(db.Text, nullable=True)        # Guarda como texto separado por comas
    footer = db.Column(db.Text, nullable=True)