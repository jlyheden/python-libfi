import unittest
import datetime
import json
from libfi.util import TransactionJSONDecoder, TransactionJSONEncoder
from libfi.domain import Transaction


class TestTransactionJSONEncoder(unittest.TestCase):

    def test_encode_transaction(self):
        transaction = Transaction(
            publication_date=datetime.date(2020, 3, 10),
            issuer="mr issuer",
            person="mrs person",
            position="x",
            closely_associated=True,
            nature_of_transaction="fun and games",
            instrument_name="some company",
            isin="1234",
            transaction_date=datetime.date(2020, 3, 9),
            volume=10,
            unit=1,
            price=10.23,
            currency="SEK",
            trading_venue="stock market",
            status=""
        )
        json_output = json.dumps(transaction, cls=TransactionJSONEncoder)


class TestTransactionJSONDecoder(unittest.TestCase):

    def test_decode_transaction(self):
        j = """
        {
          "publication_date": "2020-03-10",
          "issuer": "mr issuer",
          "person": "mrs person",
          "position": "x",
          "closely_associated": true,
          "nature_of_transaction": "fun and games",
          "instrument_name": "some company",
          "isin": "1234",
          "transaction_date": "2020-03-09",
          "volume": 10,
          "unit": 1,
          "price": 10.23,
          "currency": "SEK",
          "trading_venue": "stock market",
          "status": ""
        }
        """
        transaction = json.loads(j, cls=TransactionJSONDecoder)
        self.assertIsInstance(transaction.publication_date, datetime.date)
        self.assertIsInstance(transaction.transaction_date, datetime.date)
        self.assertIsInstance(transaction, Transaction)

    def test_decode_transaction_list(self):
        j = """
        [
            {
              "publication_date": "2020-03-10",
              "issuer": "mr issuer",
              "person": "mrs person",
              "position": "x",
              "closely_associated": true,
              "nature_of_transaction": "fun and games",
              "instrument_name": "some company",
              "isin": "1234",
              "transaction_date": "2020-03-09",
              "volume": 10,
              "unit": 1,
              "price": 10.23,
              "currency": "SEK",
              "trading_venue": "stock market",
              "status": ""
            }
        ]
                """
        transactions = json.loads(j, cls=TransactionJSONDecoder)
        self.assertIsInstance(transactions[0].publication_date, datetime.date)
        self.assertIsInstance(transactions[0].transaction_date, datetime.date)
        self.assertIsInstance(transactions[0], Transaction)
