import json
from datetime import datetime
from .domain import Transaction


class TransactionJSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if isinstance(dct, list):
            transactions = []
            for item in dct:
                transactions.append(self.__get_transaction(item))
        else:
            return self.__get_transaction(dct)

    @staticmethod
    def __get_transaction(dct):
        dct["publication_date"] = datetime.fromisoformat(dct["publication_date"]).date()
        dct["transaction_date"] = datetime.fromisoformat(dct["transaction_date"]).date()
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
                "volume": obj.volume,
                "unit": obj.unit,
                "price": obj.price,
                "currency": obj.currency,
                "trading_venue": obj.trading_venue,
                "status": obj.status
            }
        return json.JSONEncoder.default(self, obj)
