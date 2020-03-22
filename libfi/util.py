import json
import time
import logging
import random
from datetime import datetime
from decimal import Decimal
from .domain import Transaction

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def random_delay(func):
    """
    If set in decorated object then wait between configured duration to perform action
    Relies on add_random_delay, random_delay_min, random_delay_min to be set in self

    :param func:
    :return:
    """
    def _decorator(self, *args, **kwargs):
        try:
            if self.add_random_delay:
                delay = random.randint(self.random_delay_min, self.random_delay_max)
                LOGGER.info("Inserted random delay for {}s".format(delay))
                time.sleep(delay)
        except AttributeError as e:
            LOGGER.exception("Failed to insert random_delay", e)
        return func(self, *args, **kwargs)
    return _decorator


class TransactionJSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if isinstance(dct, list):
            transactions = []
            for item in dct:
                transactions.append(self.__transaction_from_dict(item))
        else:
            return self.__transaction_from_dict(dct)

    @staticmethod
    def __transaction_from_dict(dct):
        dct["publication_date"] = datetime.fromisoformat(dct["publication_date"]).date()
        dct["transaction_date"] = datetime.fromisoformat(dct["transaction_date"]).date()
        dct["volume"] = Decimal(dct["volume"])
        dct["price"] = Decimal(dct["price"])
        return Transaction(**dct)


class TransactionJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Transaction):
            return {
                "publication_date": obj.publication_date.isoformat(),
                "issuer": obj.issuer,
                "person": obj.person,
                "position": obj.position,
                "closely_associated": obj.closely_associated,
                "nature_of_transaction": obj.nature_of_transaction,
                "instrument_name": obj.instrument_name,
                "isin": obj.isin,
                "transaction_date": obj.transaction_date.isoformat(),
                "volume": str(obj.volume),
                "unit": obj.unit,
                "price": str(obj.price),
                "currency": obj.currency,
                "trading_venue": obj.trading_venue,
                "status": obj.status
            }
        return json.JSONEncoder.default(self, obj)
