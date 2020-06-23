import unittest
import json

from app import application, db


class OrderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = application.test_client()
        self.db = db.get_db()

    def tearDown(self) -> None:
        self.db.drop_collection('order')

    def test_bad_request_missing_fruits(self):
        resp = self.app.post('/order', json={
            "date": 1,
            "fake": {
                "mango": 5,
                "orange": 10
            }
        })
        self.assertEqual(resp.status_code, 400)

    def test_bad_request_not_number(self):
        resp = self.app.post('/order', json={
            "date": 1,
            "fruits": {
                "mango": "not_a_number",
            }
        })
        self.assertEqual(resp.status_code, 400)

    def test_bad_request_missing_date(self):
        resp = self.app.post('/order', json={
            "data": 1,
            "fruits": {
                "mango": 5,
                "orange": 10
            }
        })
        self.assertEqual(resp.status_code, 400)

    def test_normal_case1(self):
        resp = self.app.post('/order', json={
            "date": 1,
            "fruits": {
                "mango": 5,
                "orange": 10
            }
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['status'], True)


if __name__ == '__main__':
    unittest.main()