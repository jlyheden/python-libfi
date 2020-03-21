import unittest
import datetime
import json
from libfi.util import TransactionJSONDecoder, TransactionJSONEncoder
from libfi.domain import Transaction


class TestTransactionJSONEncoderDecoder(unittest.TestCase):

    def test_encode_and_decode_transaction(self):
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
        transaction_json = json.dumps(transaction, cls=TransactionJSONEncoder)
        transaction_decoded = json.loads(transaction_json, cls=TransactionJSONDecoder)
        self.assertEqual(transaction, transaction_decoded)

    def test_encode_and_decode_transaction_list(self):
        transactions = [
            Transaction(
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
            ]
        transactions_json = json.dumps(transactions, cls=TransactionJSONEncoder)
        transactions_decoded = json.loads(transactions_json, cls=TransactionJSONDecoder)
        self.assertEqual(transactions[0], transactions_decoded[0])
