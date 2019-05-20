import unittest
from init_db import create_db
from test_variables import FILE_NAME
from transactions import Transactions

import os

class TestTransactions(unittest.TestCase):
    def test_create_transaction(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)

        c = trs.create_transaction(-20000, 1)
        ts = c[2]
        self.assertEqual((1, -20000, ts, 1), c)

        os.remove(FILE_NAME)

    def test_update_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)
        trs.create_transaction(10, 1 )

        c = trs.update_id(id=1, amount=20, account_fk=2)
        ts = c[2]
        self.assertEqual((1, 20, ts, 2), c)

        c = trs.update_id(id=1, amount=10)
        ts = c[2]
        self.assertEqual((1, 10, ts, 2), c)

        c = trs.update_id(id=1, account_fk=1)
        ts = c[2]
        self.assertEqual((1, 10, ts, 1), c)

        c = trs.update_id(id=1, amount=0)
        ts = c[2]
        self.assertEqual((1, 0, ts, 1), c)

        os.remove(FILE_NAME)

    def test_delete_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)
        trs.create_transaction(10, 1)
        trs.create_transaction(20, 1)

        c = trs.delete_id(1)
        self.assertEqual(True, c)

        c = trs.delete_id(2)
        self.assertEqual(True, c)

        os.remove(FILE_NAME)

    def test_retrieve_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)
        trs.create_transaction(10, 1)

        c = trs.retrieve_id(id=1)
        ts = c[2]
        self.assertEqual((1, 10, ts, 1), c)

        os.remove(FILE_NAME)

    def test_retrieve_transactions(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)
        trs.create_transaction(10, 1)
        trs.create_transaction(20, 1)

        c = trs.retrieve_transactions()
        ts1 = c[0][2]
        ts2 = c[1][2]
        self.assertEqual([(1, 10, ts1, 1), (2, 20, ts2, 1)], c)

        os.remove(FILE_NAME)

    def test_retrieve_transactions_for_account(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        trs = Transactions(FILE_NAME)
        trs.create_transaction(10, 1)
        trs.create_transaction(20, 2)
        trs.create_transaction(30, 1)
        trs.create_transaction(40, 3)

        c = trs.retrieve_transactions_for_account(1)
        ts1 = c[0][2]
        ts2 = c[1][2]
        self.assertEqual([(1, 10, ts1, 1), (3, 30, ts2, 1)], c)

        os.remove(FILE_NAME)


if __name__ == '__main__':
    unittest.main()
