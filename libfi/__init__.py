import backoff
from requests import get
from requests.exceptions import RequestException
from lxml import html
from datetime import datetime
from decimal import Decimal


def parse_page(content):
    transactions = []
    tree = html.fromstring(content)
    for t in tree.xpath('//tbody/tr'):
        columns = [x.text for x in t.findall('td')]
        transactions.append(Transaction(columns))
    return transactions


class Transaction(object):

    def __init__(self, columns):
        self.publication_date = datetime.strptime(columns[0], "%d/%m/%Y")
        self.issuer = columns[1]
        self.person = columns[2]
        self.position = columns[3]
        self.closely_associated = False if columns[4] is None else columns[4].lower() == "yes"
        self.nature_of_transaction = columns[5]
        self.instrument_name = columns[6]
        self.isin = columns[7]
        self.transaction_date = datetime.strptime(columns[8], "%d/%m/%Y")
        self.volume = Decimal(columns[9])
        self.unit = columns[10]
        self.price = Decimal(columns[11])
        self.currency = columns[12]
        self.trading_venue = columns[13]
        self.status = columns[14]

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


class Client(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
        }

    def get_all_transactions(self, publication_date):
        t = []
        i = 1
        eol = False
        while not eol:
            transactions = parse_page(self.__get_page(i))
            for transaction in transactions:
                if transaction.publication_date == publication_date:
                    t.append(transaction)
                elif transaction.publication_date > publication_date:
                    continue
                else:
                    eol = True
                    break
            i += 1
        return t

    @backoff.on_exception(backoff.expo, RequestException, max_tries=10)
    def __get_page(self, index):
        req = get("https://marknadssok.fi.se/Publiceringsklient/en-GB/Search/Search?SearchFunctionType=Insyn&button"
                  "=search&Page={}".format(index), headers=self.headers)
        req.raise_for_status()
        return req.content


class StatisticsHelper(object):

    def __init__(self, transactions, **kwargs):
        """

        :param transactions: list of transactions
        :type transactions: list of Transaction
        """
        self.ignore_venues = kwargs.get("ignore_venues", [])
        self.transactions = transactions

    def get_total_transactions_by_company(self):
        c = dict()
        for t in self.transactions:
            if t.trading_venue in self.ignore_venues:
                continue
            if t.instrument_name not in c:
                c[t.instrument_name] = 0
            s = t.volume * t.price
            if t.nature_of_transaction == "Acquisition":
                c[t.instrument_name] += s
            elif t.nature_of_transaction == "Disposal":
                c[t.instrument_name] -= s
        return {k: v for (k, v) in c.items() if v}

    def get_top_buyers_by_company(self, limit=None):
        r = {k: v for (k, v) in self.get_total_transactions_by_company().items() if v > 0}
        s = sorted(r.items(), key=lambda kv: kv[1], reverse=True)
        if limit and len(s) > limit:
            return s[0:limit]
        else:
            return s

    def get_top_sellers_by_company(self, limit=None):
        r = {k: v for (k, v) in self.get_total_transactions_by_company().items() if v < 0}
        s = sorted(r.items(), key=lambda kv: kv[1])
        if limit and len(s) > limit:
            return s[0:limit]
        else:
            return s
