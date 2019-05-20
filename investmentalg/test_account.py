import unittest
from init_db import create_db
from test_variables import FILE_NAME
from account import Account
import os


class TestAccount(unittest.TestCase):

        def _init_test(self):
            if os.path.isfile(FILE_NAME):
                os.remove(FILE_NAME)
            create_db(FILE_NAME)
            return Account(FILE_NAME)

        def test_create_account(self):
            acc = self._init_test()

            c = acc.create_account("farhan", fee=2, risk=0.3, profit=0.5, fund_id=1)
            ts = c[3]
            self.assertEqual((1, "farhan", 0.0, ts, 2,  0.3, 0.5, 1, c[-1]), c)

            os.remove(FILE_NAME)

        def test_update_id(self):
            acc = self._init_test()

            acc.create_account("farhan", fee=1, risk=0.3 , profit=0.6, fund_id=1)

            c = acc.update_id(id=1, name="saeid", percentage=0.2, fee=2, risk=0.4, profit=0.5, fund_fk=2)
            self.assertEqual((1, "saeid", 0.2, c[3], 2, 0.4, 0.5, 2, c[-1]), c)

            c = acc.update_id(id=1, name="farhan")
            self.assertEqual((1, "farhan", 0.2, c[3], 2, 0.4, 0.5, 2, c[-1]), c)

            c = acc.update_id(id=1, percentage=0.5)
            self.assertEqual((1, "farhan", 0.5, c[3], 2, 0.4, 0.5, 2, c[-1]), c)

            c = acc.update_id(id=1, fee=3)
            self.assertEqual((1, "farhan", 0.5, c[3], 3, 0.4, 0.5, 2, c[-1]), c)

            c = acc.update_id(id=1, risk=1)
            self.assertEqual((1, "farhan", 0.5, c[3], 3, 1, 0.5, 2, c[-1]), c)

            c = acc.update_id(id=1, profit=0.4)
            self.assertEqual((1, "farhan", 0.5, c[3], 3, 1, 0.4, 2, c[-1]), c)

            c = acc.update_id(id=1, fund_fk=1)
            self.assertEqual((1, "farhan", 0.5, c[3], 3, 1, 0.4, 1, c[-1]), c)

            c = acc.update_id(id=1, name="saeid", percentage=0.2, fee=2, risk=0.4, profit=0.5, fund_fk=2, password='1234')
            self.assertEqual((1, "saeid", 0.2, c[3], 2, 0.4, 0.5, 2, '1234'), c)

            c = acc.update_id(id=1, password='4321')
            self.assertEqual((1, "saeid", 0.2, c[3], 2, 0.4, 0.5, 2, '4321'), c)


            os.remove(FILE_NAME)

        def test_delete_id(self):
            acc = self._init_test()
            acc.create_account("farhan0", fee=2, risk=0.3, profit=0.5, fund_id=1)
            acc.create_account("farhan1", fee=2, risk=0.3, profit=0.5, fund_id=2)

            c = acc.delete_id(1)
            self.assertEqual(True, c)

            c = acc.delete_id(2)
            self.assertEqual(True, c)

            os.remove(FILE_NAME)

        def test_retrieve_id(self):
            acc = self._init_test()
            acc.create_account("farhan", fee=2, risk=0.3, profit=0.5, fund_id=1)

            c = acc.retrieve_id(id=1)
            ts = c[3]
            self.assertEqual((1, "farhan", 0.0, c[3], 2, 0.3, 0.5, 1, c[-1]), c)

            os.remove(FILE_NAME)

        def test_retrieve_accounts(self):
            acc = self._init_test()
            acc.create_account("farhan", fee=0.3, risk=0.3, profit=0.3, fund_id=1)

            c = acc.retrieve_accounts()
            self.assertEqual([(1, "farhan", 0.0, c[0][3], 0.3, 0.3, 0.3, 1, c[0][-1])], c)

            os.remove(FILE_NAME)

        def test_retrieve_accounts_for_portfolio(self):
            acc = self._init_test()
            acc.create_account("farhan0", fee=0.3, risk=0.3, profit=0.3, fund_id=1)
            acc.create_account("farhan1",  fee=0.3, risk=0.3, profit=0.3, fund_id=2)
            acc.create_account("farhan2",  fee=0.3, risk=0.3, profit=0.3, fund_id=1)
            acc.create_account("farhan3",  fee=0.3, risk=0.3, profit=0.3, fund_id=3)

            c = acc.retrieve_accounts_for_portfolio(1)
            self.assertEqual([(1, "farhan0", 0.0, c[0][3], 0.3, 0.3, 0.3, 1, c[0][-1]), (3, "farhan2", 0.0, c[1][3], 0.3, 0.3, 0.3, 1, c[1][-1])], c)

            os.remove(FILE_NAME)



if __name__ == '__main__':
    unittest.main()
