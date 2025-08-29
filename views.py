from flask import Blueprint, request, jsonify  # Importa herramientas de Flask para rutas y respuestas
from models import db, InputData, ScrapedData  # Importa los modelos de la base de datos
from selenium import webdriver  # Importa Selenium para web scraping
from selenium.webdriver.chrome.options import Options  # Opciones para el navegador Chrome
from selenium.webdriver.common.by import By  # Para seleccionar elementos por tipo
from selenium.webdriver.chrome.service import Service  # Servicio para el driver de Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Descarga y gestiona el driver de Chrome
import requests  # Importa requests para hacer peticiones HTTP
from bs4 import BeautifulSoup  # Importa BeautifulSoup para analizar HTML

bp = Blueprint('main', __name__)  # Crea un blueprint para organizar las rutas

@bp.route('/', methods=['GET'])
def index():
    return "Hello, World!"  # Ruta principal, solo devuelve un saludo

@bp.route('/ejemplo', methods=['POST'])
def tutorial():
    data = request.get_json()  # Obtiene el JSON enviado en el body
    if not data or 'mensaje' not in data:  # Si falta el campo 'mensaje', devuelve error
        return jsonify({'error': 'Falta el campo \"mensaje\"'}), 400
    mensaje = data['mensaje']  # Extrae el mensaje del JSON
    respuesta = f"Recibido: {mensaje}"  # Prepara la respuesta
    return jsonify({'respuesta': respuesta})  # Devuelve la respuesta en formato JSON

@bp.route('/data', methods=['GET'])
def get_data():
    records = InputData.query.all()  # Consulta todos los registros de InputData
    result = [{'id': r.id, 'input_value': r.input_value, 'output_value': r.output_value} for r in records]
    return jsonify(result)  # Devuelve la lista en formato JSON

@bp.route('/scrape_simple', methods=['GET'])
def scrape_simple():
    """
    Realiza web scraping con Selenium sin esperar contenido dinámico y guarda los datos en la tabla ScrapedData.
    """
    url = 'https://corferias.com/'  # URL de la página a scrapear

    # Configura el navegador Chrome en modo headless (sin ventana)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicializa el navegador Chrome usando webdriver-manager para el driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)  # Abre la página web

    # Obtiene el título de la página
    title = driver.title

    # Obtiene el texto alternativo del logo (si existe)
    try:
        element = driver.find_element(By.CLASS_NAME, 'nav-logo')
        logo_text = element.get_attribute('alt')
    except Exception:
        logo_text = None

    # Obtiene los primeros 5 enlaces de la página
    links = []
    try:
        links_elements = driver.find_elements(By.TAG_NAME, 'a')
        for a in links_elements:
            href = a.get_attribute('href')
            if href:
                links.append(href)
            if len(links) >= 5:
                break
    except Exception:
        links = []

    # Obtiene las primeras 5 categorías principales del menú
    categories = []
    try:
        categories_elements = driver.find_elements(By.CSS_SELECTOR, '.nav-menu-item-text')
        for cat in categories_elements:
            categories.append(cat.text)
            if len(categories) >= 5:
                break
    except Exception:
        categories = []

    # Obtiene los banners principales
    banners = []
    try:
        banners_elements = driver.find_elements(By.CSS_SELECTOR, '.nav-header')
        for banner in banners_elements:
            banners.append(banner.text)
    except Exception:
        banners = []

    # Obtiene los primeros 5 botones destacados
    buttons = []
    try:
        buttons_elements = driver.find_elements(By.CSS_SELECTOR, 'a.dynamic-access-card-item__item-title')
        for btn in buttons_elements:
            buttons.append(btn.text)
            if len(buttons) >= 5:
                break
    except Exception:
        buttons = []

    # Obtiene el texto del footer
    try:
        footer_element = driver.find_element(By.TAG_NAME, 'footer')
        footer = footer_element.text
    except Exception:
        footer = None

    driver.quit()  # Cierra el navegador

    # Inserta los datos en la tabla ScrapedData
    scraped = ScrapedData(
        title=title,
        logo_text=logo_text,
        links="|".join(links),
        categories="|".join(categories),
        banners="|".join(banners),
        buttons="|".join(buttons),
        footer=footer
    )
    db.session.add(scraped)
    db.session.commit()

    # Devuelve los datos extraídos como respuesta JSON
    return jsonify({
        'title': title,
        'logo_text': logo_text,
        'links': links,
        'categories': categories,
        'banners': banners,
        'buttons': buttons,
        'footer': footer
    })

@bp.route('/scrape_bs', methods=['GET'])
def scrape_bs():
    """
    Realiza web scraping usando requests y BeautifulSoup y guarda los datos en la tabla ScrapedData.
    """
    url = 'https://www.tiendanube.com/blog/ejemplos-paginas-web-estaticas/'  # URL de la página a scrapear
    response = requests.get(url)  # Realiza la petición HTTP
    soup = BeautifulSoup(response.text, 'html.parser')  # Analiza el HTML de la respuesta

    # Título de la página
    title = soup.title.string if soup.title else None

    # Texto alternativo del logo
    logo = soup.find('img', {'class': 'nav-logo'})
    logo_text = logo['alt'] if logo and logo.has_attr('alt') else None

    # Primeros 5 enlaces
    links = []
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
        if len(links) >= 5:
            break

    # Primeras 5 categorías principales
    categories = []
    for cat in soup.select('.nav-menu-item-text'):
        categories.append(cat.get_text(strip=True))
        if len(categories) >= 5:
            break

    # Banners principales
    banners = [banner.get_text(strip=True) for banner in soup.select('.nav-header')]

    # Primeros 5 botones destacados
    buttons = []
    for btn in soup.select('a.dynamic-access-card-item__item-title'):
        buttons.append(btn.get_text(strip=True))
        if len(buttons) >= 5:
            break

    # Footer
    footer = None
    footer_tag = soup.find('footer')
    if footer_tag:
        footer = footer_tag.get_text(strip=True)

    # Inserta los datos en la tabla ScrapedData
    scraped = ScrapedData(
        title=title,
        logo_text=logo_text,
        links="|".join(links),
        categories="|".join(categories),
        banners="|".join(banners),
        buttons="|".join(buttons),
        footer=footer
    )
    db.session.add(scraped)
    db.session.commit()

    # Devuelve los datos extraídos como respuesta JSON
    return jsonify({
        'title': title,
        'logo_text': logo_text,
        'links': links,
        'categories': categories,
        'banners': banners,
        'buttons': buttons,
        'footer': footer
    })

@bp.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()  # Obtiene el JSON enviado en el body
    if not data or 'input_value' not in data or 'output_value' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    new_record = InputData(
        input_value=data['input_value'],
        output_value=data['output_value']
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({
        'id': new_record.id,
        'input_value': new_record.input_value,
        'output_value': new_record.output_value
    }), 201

@bp.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()  # Obtiene el JSON enviado en el body
    record = InputData.query.get(id)  # Busca el registro por ID
    if not record:
        return jsonify({'error': 'Registro no encontrado'}), 404
    record.input_value = data.get('input_value', record.input_value)
    record.output_value = data.get('output_value', record.output_value)
    db.session.commit()
    return jsonify({'id': record.id, 'input_value': record.input_value, 'output_value': record.output_value})

@bp.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    record = InputData.query.get(id)  # Busca el registro por ID
    if not record:
        return jsonify({'error': 'Registro no encontrado'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Registro eliminado'})