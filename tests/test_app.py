import unittest

from app import app


class Pages(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_records(self):
        response = self.client.get('/records/assignments')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get('/detail/assignments/1')
        self.assertEqual(response.status_code, 200)

    def test_invalid(self):
        response = self.client.get('/records/ground_truth')
        self.assertEqual(response.status_code, 404)

    def test_filters(self):
        response = self.client.get(
            '/records/submissions?q=missing&status=missing&page=2'
        )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()