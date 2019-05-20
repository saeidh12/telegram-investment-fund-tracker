import unittest
from init_db import create_db
from test_variables import FILE_NAME
from funds import Funds
import os

class TestFunds(unittest.TestCase):
    def test_create_Fund(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        fund = Funds(FILE_NAME)

        c = fund.create_fund(-20000, 1)
        ts = c[2]
        self.assertEqual((1, -20000, ts, 1), c)

        os.remove(FILE_NAME)

    def test_update_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        fund = Funds(FILE_NAME)
        fund.create_fund(10, 1 )

        c = fund.update_id(id=1, amount=20, account_fk=2)
        ts = c[2]
        self.assertEqual((1, 20, ts, 2), c)

        c = fund.update_id(id=1, amount=10)
        ts = c[2]
        self.assertEqual((1, 10, ts, 2), c)

        c = fund.update_id(id=1, account_fk=1)
        ts = c[2]
        self.assertEqual((1, 10, ts, 1), c)

        c = fund.update_id(id=1, amount=0)
        ts = c[2]
        self.assertEqual((1, 0, ts, 1), c)

        os.remove(FILE_NAME)

    def test_delete_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        fund = Funds(FILE_NAME)
        fund.create_fund(10, 1)
        fund.create_fund(20, 1)

        c = fund.delete_id(1)
        self.assertEqual(True, c)

        c = fund.delete_id(2)
        self.assertEqual(True, c)

        os.remove(FILE_NAME)

    def test_retrieve_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        fund = Funds(FILE_NAME)
        fund.create_fund(10, 1)

        c = fund.retrieve_id(id=1)
        ts = c[2]
        self.assertEqual((1, 10, ts, 1), c)

        os.remove(FILE_NAME)

    def test_retrieve_accounts(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        fund = Funds(FILE_NAME)
        fund.create_fund(10, 1)
        fund.create_fund(20, 1)

        c = fund.retrieve_funds()
        ts1 = c[0][2]
        ts2 = c[1][2]
        self.assertEqual([(1, 10, ts1, 1), (2, 20, ts2, 1)], c)

        os.remove(FILE_NAME)

    def test_retrieve_funds_for_account(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Funds(FILE_NAME)
        trs.create_fund(10, 1)
        trs.create_fund(20, 2)
        trs.create_fund(30, 1)
        trs.create_fund(40, 3)

        c = trs.retrieve_funds_for_account(1)
        ts1 = c[0][2]
        ts2 = c[1][2]
        self.assertEqual([(1, 10, ts1, 1), (3, 30, ts2, 1)], c)

        os.remove(FILE_NAME)


if __name__ == '__main__':
    unittest.main()
