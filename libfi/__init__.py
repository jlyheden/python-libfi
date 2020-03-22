import backoff
import logging
from requests import get
from requests.exceptions import RequestException
from lxml import html
from .domain import Transaction
from .util import random_delay

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def parse_page(content):
    transactions = []
    tree = html.fromstring(content)
    for t in tree.xpath('//tbody/tr'):
        columns = [x.text for x in t.findall('td')]
        transactions.append(Transaction.factory(columns))
    return transactions


class Client(object):

    def __init__(self, add_random_delay=False, random_delay_min=5, random_delay_max=10):
        """
        Initialises a libfi client

        :param add_random_delay: introduces delays between individual calls to external service
        :type add_random_delay: bool
        :param random_delay_min: min number of seconds
        :type random_delay_min: int
        :param random_delay_max: max number of seconds
        :type random_delay_max: int
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
        }
        self.add_random_delay = add_random_delay
        self.random_delay_min = random_delay_min
        self.random_delay_max = random_delay_max

    def get_all_transactions(self, publication_date):
        """
        Fetches all transactions matching the publication_date

        :param publication_date: matching publication_date
        :type publication_date: datetime.date
        :return: transactions
        :rtype: list of Transaction
        """
        t = []
        i = 1
        eol = False
        while not eol:
            transactions = parse_page(self.__get_page(i))
            for transaction in transactions:
                if transaction.publication_date == publication_date:
                    LOGGER.debug("Adding transaction to list: {}".format(transaction))
                    t.append(transaction)
                elif transaction.publication_date > publication_date:
                    continue
                else:
                    eol = True
                    break
            i += 1
        return t

    @random_delay
    @backoff.on_exception(backoff.expo, RequestException, max_tries=10)
    def __get_page(self, index):
        url = "https://marknadssok.fi.se/Publiceringsklient/en-GB/Search/Search?SearchFunctionType=Insyn&button" \
              "=search&Page={}".format(index)
        LOGGER.debug("Fetching from {}".format(url))
        req = get(url, headers=self.headers)
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
