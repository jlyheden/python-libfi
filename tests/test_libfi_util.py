import unittest
import datetime
import json
from unittest.mock import patch
from decimal import Decimal
from libfi.util import TransactionJSONDecoder, TransactionJSONEncoder, random_delay
from libfi.domain import Transaction


class FakeClient(object):

    def __init__(self, add_random_delay, random_delay_min=5, random_delay_max=10):
        self.add_random_delay = add_random_delay
        self.random_delay_min = random_delay_min
        self.random_delay_max = random_delay_max

    @random_delay
    def do_it(self, param):
        return param


class TestDecorator(unittest.TestCase):

    @patch('time.sleep', return_value=None)
    @patch('random.randint', return_value=7)
    def test_random_relay(self, patched_random_randint, patched_time_sleep):
        f = FakeClient(add_random_delay=True)
        rv = f.do_it(True)
        self.assertEqual(((7,),), patched_time_sleep.call_args)
        self.assertTrue(patched_time_sleep.called)
        self.assertTrue(rv)

    @patch('time.sleep', return_value=None)
    def test_random_relay_disabled(self, patched_time_sleep):
        f = FakeClient(add_random_delay=False)
        rv = f.do_it(True)
        self.assertFalse(patched_time_sleep.called)
        self.assertTrue(rv)


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
            volume=Decimal("10"),
            unit=1,
            price=Decimal("10.23"),
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
                volume=Decimal("10"),
                unit=1,
                price=Decimal("10.23"),
                currency="SEK",
                trading_venue="stock market",
                status=""
            )
            ]
        transactions_json = json.dumps(transactions, cls=TransactionJSONEncoder)
        transactions_decoded = json.loads(transactions_json, cls=TransactionJSONDecoder)
        self.assertEqual(transactions[0], transactions_decoded[0])
