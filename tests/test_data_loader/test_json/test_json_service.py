from order_app.data_loader.json.json_service import load_from_json

import unittest


class TestJsonService(unittest.TestCase):

    def test_load_from_json(self):
        expected_result = [
            {'customer': {'name': 'JOHN', 'surname': 'MAYER', 'age': 24, 'email': 'johnmayer@gmail.com'},
             'product': {'name': 'LAPTOP', 'price': 5300, 'category': 'A'}, 'quantity': 1,
             'order_date': '12-06-2024'},
            {'customer': {'name': 'ANNA', 'surname': 'SNOW', 'age': 36, 'email': 'ann45snow@gmail.com'},
             'product': {'name': 'TV', 'price': 2400, 'category': 'A'}, 'quantity': 3,
             'order_date': '12-06-2024'},
            {'customer': {'name': 'ALBERT', 'surname': 'GILBERT', 'age': 13, 'email': 'gilbertgod@gmail.com'},
             'product': {'name': 'car', 'price': 25000, 'category': 'B'}, 'quantity': 2,
             'order_date': '01-06-2023'},
            {'customer': {'name': 'JOHN', 'surname': 'MAYER', 'age': 24, 'email': 'johnmayer@gmail.com'},
             'product': {'name': 'LAPTOP', 'price': 5300, 'category': 'C'}, 'quantity': 1,
             'order_date': '12-06-2024'},
            {'customer': {'name': 'ANNA', 'surname': 'SNOW', 'age': 36, 'email': 'ann45snow@gmail.com'},
             'product': {'name': 'TV', 'price': 2400, 'category': 'C'}, 'quantity': 3,
             'order_date': '12-06-2024'},
            {'customer': {'name': 'ALBERT', 'surname': 'GILBERT', 'age': 13, 'email': 'gilbertgod@gmail.com'},
             'product': {'name': 'car', 'price': 25000, 'category': 'B'}, 'quantity': 2,
             'order_date': '01-01-2023'}]
        result = load_from_json('order_app/data/orders.json')

        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
