from flask import Blueprint, request, jsonify
from models import db, InputData
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@bp.route('/ejemplo', methods=['POST'])
def tutorial():
    data = request.get_json()
    if not data or 'mensaje' not in data:
        return jsonify({'error': 'Falta el campo \"mensaje\"'}), 400
    mensaje = data['mensaje']
    respuesta = f"Recibido: {mensaje}"
    return jsonify({'respuesta': respuesta})

@bp.route('/data', methods=['GET'])
def get_data():
    records = InputData.query.all()
    result = [{'id': r.id, 'input_value': r.input_value, 'output_value': r.output_value} for r in records]
    return jsonify(result)

from models import db, InputData, ScrapedData

@bp.route('/scrape')
def scrape():
    url = 'https://www.mercadolibre.com.co/'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    title = driver.title

    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-logo')))
        logo_text = element.get_attribute('alt')
    except Exception:
        logo_text = None

    try:
        links_elements = driver.find_elements(By.TAG_NAME, 'a')
        links = [a.get_attribute('href') for a in links_elements if a.get_attribute('href')]
    except Exception:
        links = []

    try:
        categories_elements = driver.find_elements(By.CSS_SELECTOR, '.nav-menu-item-text')
        categories = [cat.text for cat in categories_elements]
    except Exception:
        categories = []

    try:
        banners_elements = driver.find_elements(By.CSS_SELECTOR, '.nav-header')
        banners = [banner.text for banner in banners_elements]
    except Exception:
        banners = []

    try:
        buttons_elements = driver.find_elements(By.CSS_SELECTOR, 'a.dynamic-access-card-item__item-title')
        buttons = [btn.text for btn in buttons_elements]
    except Exception:
        buttons = []

    try:
        footer_element = driver.find_element(By.TAG_NAME, 'footer')
        footer = footer_element.text
    except Exception:
        footer = None

    driver.quit()

    # Guarda los datos en la nueva tabla ScrapedData
    scraped = ScrapedData(
        title=title,
        logo_text=logo_text,
        links="|".join(links[:5]),           # Guarda solo los primeros 5 enlaces, separados por |
        categories="|".join(categories[:5]), # Guarda solo los primeros 5, separados por |
        banners="|".join(banners),
        buttons="|".join(buttons[:5]),
        footer=footer
    )
    db.session.add(scraped)
    db.session.commit()

    return jsonify({
        'title': title,
        'logo_text': logo_text,
        'links': links[:5],
        'categories': categories[:5],
        'banners': banners,
        'buttons': buttons[:5],
        'footer': footer
    })

@bp.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
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
    data = request.get_json()
    record = InputData.query.get(id)
    if not record:
        return jsonify({'error': 'Registro no encontrado'}), 404
    record.input_value = data.get('input_value', record.input_value)
    record.output_value = data.get('output_value', record.output_value)
    db.session.commit()
    return jsonify({'id': record.id, 'input_value': record.input_value, 'output_value': record.output_value})

@bp.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    record = InputData.query.get(id)
    if not record:
        return jsonify({'error': 'Registro no encontrado'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Registro eliminado'})