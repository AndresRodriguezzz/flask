import unittest  # Importa el módulo de pruebas unitarias
from app import app  # Importa la aplicación Flask

class APITestCase(unittest.TestCase):  # Clase para pruebas de la API
    def setUp(self):
        self.client = app.test_client()  # Crea un cliente de pruebas

    def test_index(self):
        response = self.client.get('/')  # Prueba la ruta principal
        self.assertEqual(response.status_code, 200)  # Debe responder 200 OK

    def test_scrape(self):
        response = self.client.get('/scrape')  # Prueba el endpoint de scraping
        self.assertEqual(response.status_code, 200)  # Debe responder 200 OK

    def test_add_data(self):
        response = self.client.post('/add_data', json={
            'input_value': 'test',
            'output_value': 'test'
        })  # Prueba el endpoint para agregar datos
        self.assertEqual(response.status_code, 201)  # Debe responder 201 Created

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas