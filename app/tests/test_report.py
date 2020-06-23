import unittest
import json

from app import application, db


class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.app = application.test_client()
        self.db = db.get_db()

    def tearDown(self) -> None:
        self.db.drop_collection('order')

    def test_normalcase1(self):
        self.app.post('/order', json={
            "date": 1,
            "fruits": {
                "mango": 5,
                "orange": 10
            }
        })
        resp = self.app.get('/report?from=1&to=1')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json, {"status": True, "data": {
            "mango": 5.0,
            "orange": 10.0
        }})

    def test_normalcase2(self):
        self.app.post('/order', json={
            "date": 1,
            "fruits": {
                "mango": 5,
                "orange": 10
            }
        })
        self.app.post('/order', json={
            "date": 3,
            "fruits": {
                "mango": 5,
                "apple": 10
            }
        })
        resp = self.app.get('/report?from=1&to=2')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json, {"status": True, "data": {
            "mango": 5.0,
            "orange": 10.0
        }})
        resp = self.app.get('/report?from=1&to=3')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json, {"status": True, "data": {
            "mango": 10.0,
            "orange": 10.0,
            "apple": 10.0
        }})
        resp = self.app.get('/report?from=2&to=3')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json, {"status": True, "data": {
            "mango": 5.0,
            "apple": 10.0
        }})

    def test_invalid_range(self):
        resp = self.app.get('/report?from=3&to=2')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json, {"status": True, "data": {}})

    def test_bad_request(self):
        resp = self.app.get('/report')
        self.assertEqual(resp.status_code, 400)

        resp = self.app.get('/report?from=1')
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()