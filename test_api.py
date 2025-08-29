import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_scrape(self):
        response = self.client.get('/scrape')
        self.assertEqual(response.status_code, 200)

    def test_add_data(self):
        response = self.client.post('/add_data', json={
            'input_value': 'test',
            'output_value': 'test'
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()