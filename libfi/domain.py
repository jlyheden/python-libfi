from datetime import datetime
from decimal import Decimal


class Transaction(object):

    def __init__(self, **kwargs):
        self.publication_date = kwargs.get("publication_date")
        self.issuer = kwargs.get("issuer")
        self.person = kwargs.get("person")
        self.position = kwargs.get("position")
        self.closely_associated = kwargs.get("closely_associated")
        self.nature_of_transaction = kwargs.get("nature_of_transaction")
        self.instrument_name = kwargs.get("instrument_name")
        self.isin = kwargs.get("isin")
        self.transaction_date = kwargs.get("transaction_date")
        self.volume = kwargs.get("volume")
        self.unit = kwargs.get("unit")
        self.price = kwargs.get("price")
        self.currency = kwargs.get("currency")
        self.trading_venue = kwargs.get("trading_venue")
        self.status = kwargs.get("status")

    def __repr__(self):
        return "<Transaction(publication_date={}, issuer={}, person={}, position={}, closely_associated={}, " \
               "nature_of_transaction={}, instrument_name={}, isin={}, transaction_date={}, volume={}, unit={}, " \
               "price={}, currency={}, trading_venue={}, status={})> ".format(self.publication_date, self.issuer,
                                                                              self.person, self.position,
                                                                              self.closely_associated,
                                                                              self.nature_of_transaction,
                                                                              self.instrument_name, self.isin,
                                                                              self.transaction_date, self.volume,
                                                                              self.unit, self.price, self.currency,
                                                                              self.trading_venue, self.status)

    @classmethod
    def factory(cls, columns):
        return Transaction(
            publication_date=datetime.strptime(columns[0], "%d/%m/%Y").date(),
            issuer=columns[1],
            person=columns[2],
            position=columns[3],
            closely_associated=False if columns[4] is None else columns[4].lower() == "yes",
            nature_of_transaction=columns[5],
            instrument_name=columns[6],
            isin=columns[7],
            transaction_date=datetime.strptime(columns[8], "%d/%m/%Y").date(),
            volume=Decimal(columns[9]),
            unit=columns[10],
            price=Decimal(columns[11]),
            currency=columns[12],
            trading_venue=columns[13],
            status=columns[14]
        )