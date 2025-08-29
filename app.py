from flask import Flask  # Importa la clase principal de Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS  # Importa la configuración de la base de datos
from models import db  # Importa la instancia de la base de datos
from views import bp  # Importa el blueprint con las rutas


app = Flask(__name__)  # Crea la aplicación Flask

# Configura la URI de la base de datos y si se deben rastrear las modificaciones
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)  # Inicializa la base de datos con la aplicación Flask
app.register_blueprint(bp)  # Registra el blueprint con las rutas en la aplicación

if __name__ == '__main__':  # Si el archivo se ejecuta directamente
    with app.app_context():  # Crea el contexto de la aplicación
        db.create_all()  # Crea todas las tablas en la base de datos si no existen
    app.run(debug=True, port=8000)  # Inicia el servidor Flask en modo debug y puerto 8000
