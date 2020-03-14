import unittest
import os
import vcr
from libfi import parse_page, Client, StatisticsHelper
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestParsePage(unittest.TestCase):

    def setUp(self) -> None:
        with open(os.path.join(dir_path, "resources", "index.html"), "r") as f:
            self.content = f.read()

    def test_parse_page(self):
        result = parse_page(self.content)
        self.assertEqual(10, len(result))


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        self.client = Client()

    @vcr.use_cassette(os.path.join(dir_path, 'resources/fixtures/vcr_cassettes/13_03_2020.yaml'))
    def test_get_all_transactions(self):
        pd = datetime.strptime("13/03/2020", "%d/%m/%Y")
        result = self.client.get_all_transactions(pd)
        self.assertEqual(217, len(result))


class TestStatistics(unittest.TestCase):

    def setUp(self) -> None:
        self.client = Client()

    @vcr.use_cassette(os.path.join(dir_path, 'resources/fixtures/vcr_cassettes/13_03_2020.yaml'))
    def test_get_total_transactions_by_company(self):
        pd = datetime.strptime("13/03/2020", "%d/%m/%Y")
        transactions = self.client.get_all_transactions(pd)
        stats = StatisticsHelper(transactions, ignore_venues=["Outside a trading venue"])
        stats.get_total_transactions_by_company()

    @vcr.use_cassette(os.path.join(dir_path, 'resources/fixtures/vcr_cassettes/13_03_2020.yaml'))
    def test_get_top_buyers_by_company(self):
        pd = datetime.strptime("13/03/2020", "%d/%m/%Y")
        transactions = self.client.get_all_transactions(pd)
        stats = StatisticsHelper(transactions, ignore_venues=["Outside a trading venue"])
        r = stats.get_top_buyers_by_company(limit=5)
        self.assertEqual(5, len(r))

    @vcr.use_cassette(os.path.join(dir_path, 'resources/fixtures/vcr_cassettes/13_03_2020.yaml'))
    def test_get_top_buyers_by_company(self):
        pd = datetime.strptime("13/03/2020", "%d/%m/%Y")
        transactions = self.client.get_all_transactions(pd)
        stats = StatisticsHelper(transactions, ignore_venues=["Outside a trading venue", "NORDIC SME"])
        r = stats.get_top_sellers_by_company(limit=5)
        self.assertEqual(4, len(r))
