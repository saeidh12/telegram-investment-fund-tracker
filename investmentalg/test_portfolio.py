import unittest
from init_db import create_db
import os
from portfolio import Portfolio

from test_variables import FILE_NAME

class TestPortfolio(unittest.TestCase):

    def test_create_portfolio(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)

        c = p.create_portfolio()
        self.assertEqual((1, -1), c)
        os.remove(FILE_NAME)

    def test_update_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)
        p.create_portfolio()

        c = p.update_id(id=1, main_account=1)
        self.assertEqual((1, 1), c)


        os.remove(FILE_NAME)

    def test_retrieve_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)
        p.create_portfolio()

        c = p.retrieve_id(id=1)
        self.assertEqual((1, -1), c)
        os.remove(FILE_NAME)

    def test_retrieve_portfolios(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)
        p.create_portfolio()

        c = p.retrieve_portfolios()
        self.assertEqual([(1, -1)], c)
        os.remove(FILE_NAME)

    def test_delete_id(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)
        p.create_portfolio()

        c = p.delete_id(1)
        self.assertEqual(True, c)
        os.remove(FILE_NAME)







if __name__ =='__main__':
    unittest.main()
