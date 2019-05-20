import unittest
from init_db import create_db
import os
from algorithm import Algorithm
from portfolio import Portfolio
from transactions import Transactions
from funds import Funds

from test_variables import FILE_NAME

class TestAlgorithm(unittest.TestCase):

    def _init_test(self):
        if os.path.isfile(FILE_NAME):
            os.remove(FILE_NAME)
        create_db(FILE_NAME)
        p = Portfolio(FILE_NAME)
        prt = p.create_portfolio()
        return Algorithm(FILE_NAME, prt[0])

    def _prefill_db(self, alg):
        alg.add_account(name='01', fee=0, risk=0.7, profit=0.7, fund=0.0)
        alg.add_account(name='02', fee=50, risk=0.3, profit=0.9, fund=100.0)
        alg.add_account(name='03', fee=-50, risk=0.3, profit=0.9, fund=100.0)
        alg.add_account(name="04", fee=0, risk=0.3, profit=0.9, fund=200.0,  is_main=True)

    def test_add_account(self):
        alg = self._init_test()
        prt = Portfolio(FILE_NAME)
        fnds = Funds(FILE_NAME)

        accs = alg.add_account(name='01', fee=0, risk=0.7, profit=0.7, fund=0.0)
        self.assertEqual(0.0, alg.portfolio_total_fund)
        accounts = [(1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1])]
        self.assertEqual(accounts, accs)
        prt_data = prt.retrieve_id(1)
        self.assertEqual(-1, prt_data[-1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(0, acc_fnds[-1][1])

        accs = alg.add_account(name="03", fee=0, risk=0.3, profit=0.9, fund=100.0,  is_main=True)
        self.assertEqual(100.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '03', 1.0, accs[1][3], 0, 0.3, 0.9, 1, accs[1][-1]),
        ]
        self.assertEqual(accounts, accs)
        prt_data = prt.retrieve_id(1)
        self.assertEqual(2, prt_data[-1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(100, acc_fnds[-1][1])

        os.remove(FILE_NAME)

    def test_make_transaction(self):
        alg = self._init_test()
        self._prefill_db(alg)
        trs = Transactions(FILE_NAME)
        fnds = Funds(FILE_NAME)

        accs = alg.make_transaction('01', 100)
        self.assertEqual(500.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.2, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.2, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.2, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.4, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=1)
        self.assertEqual(100, acc_trs[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(100, acc_fnds[-1][1])

        accs = alg.make_transaction('02', -100)
        self.assertEqual(400.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.25, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.0, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.25, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.5, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=2)
        self.assertEqual(-100, acc_trs[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(0, acc_fnds[-1][1])

        accs = alg.make_transaction('03', -150)
        self.assertEqual(400.0, alg.portfolio_total_fund)
        self.assertEqual(False, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=3)
        self.assertEqual(0, len(acc_trs))
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(100, acc_fnds[-1][1])

    def test_remove_main(self):
        alg = self._init_test()
        self._prefill_db(alg)

        alg.remove_main()
        p = Portfolio(FILE_NAME)
        p_data = p.retrieve_id(1)
        self.assertEqual(-1, p_data[-1])

    def test_get_account_fund(self):
        alg = self._init_test()
        self._prefill_db(alg)

        fnd = alg.get_account_fund('01')
        self.assertEqual(0, fnd)

        fnd = alg.get_account_fund('02')
        self.assertEqual(100, fnd)

        fnd = alg.get_account_fund('00')
        self.assertEqual(False, fnd)

    def test_update_total_fund_without_main(self):
        alg = self._init_test()
        self._prefill_db(alg)
        alg.remove_main()
        fnds = Funds(FILE_NAME)

        accs = alg.update_total_fund(new_fund=800)
        self.assertEqual(800.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.25, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.25, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.5, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(0, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(200, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(200, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=4)
        self.assertEqual(400, acc_fnds[-1][1])

        accs = alg.update_total_fund(new_fund=200)
        self.assertEqual(200.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.25, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.25, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.5, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(0, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(50, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(50, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=4)
        self.assertEqual(100, acc_fnds[-1][1])

    def test_update_total_fund_with_main(self):
        alg = self._init_test()
        self._prefill_db(alg)
        fnds = Funds(FILE_NAME)

        accs = alg.update_total_fund(new_fund=800)
        self.assertEqual(800.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.2375, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.2375, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.525, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(0, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(190, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(190, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=4)
        self.assertEqual(420, acc_fnds[-1][1])

        accs = alg.update_total_fund(new_fund=200)
        self.assertEqual(200.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.73625, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.73625, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', -0.4724999999999999, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(0, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(147.25, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(147.25, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=4)
        self.assertEqual(-94.49999999999999, acc_fnds[-1][1])

    def test_internal_transaction(self):
        alg = self._init_test()
        self._prefill_db(alg)
        trs = Transactions(FILE_NAME)
        fnds = Funds(FILE_NAME)

        accs = alg.internal_transaction(sender_name='02', reciever_name='01', amount=50)
        self.assertEqual(400.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.125, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.125, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.25, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.5, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=1)
        self.assertEqual(50, acc_trs[-1][1])
        acc_trs = trs.retrieve_transactions_for_account(account_id=2)
        self.assertEqual(-50, acc_trs[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(50, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(50, acc_fnds[-1][1])

        accs = alg.internal_transaction(sender_name='02', reciever_name='01', amount=100)
        self.assertEqual(400.0, alg.portfolio_total_fund)
        self.assertEqual(False, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=1)
        self.assertEqual(50, acc_trs[-1][1])
        acc_trs = trs.retrieve_transactions_for_account(account_id=2)
        self.assertEqual(-50, acc_trs[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=1)
        self.assertEqual(50, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(50, acc_fnds[-1][1])

    def test_pay_fees(self):
        alg = self._init_test()
        self._prefill_db(alg)
        trs = Transactions(FILE_NAME)
        fnds = Funds(FILE_NAME)

        accs = alg.pay_fees()
        self.assertEqual(400.0, alg.portfolio_total_fund)
        accounts = [
            (1, '01', 0.0, accs[0][3], 0, 0.7, 0.7, 1, accs[0][-1]),
            (2, '02', 0.375, accs[1][3], 50, 0.3, 0.9, 1, accs[1][-1]),
            (3, '03', 0.125, accs[2][3], -50, 0.3, 0.9, 1, accs[2][-1]),
            (4, '04', 0.5, accs[3][3], 0, 0.3, 0.9, 1, accs[3][-1]),
        ]
        self.assertEqual(accounts, accs)
        acc_trs = trs.retrieve_transactions_for_account(account_id=2)
        self.assertEqual(50, acc_trs[-1][1])
        acc_trs = trs.retrieve_transactions_for_account(account_id=3)
        self.assertEqual(-50, acc_trs[-1][1])
        acc_trs = trs.retrieve_transactions_for_account(account_id=4)
        self.assertEqual(-50, acc_trs[-2][1])
        self.assertEqual(50, acc_trs[-1][1])

        acc_fnds = fnds.retrieve_funds_for_account(account_id=2)
        self.assertEqual(150, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=3)
        self.assertEqual(50, acc_fnds[-1][1])
        acc_fnds = fnds.retrieve_funds_for_account(account_id=4)
        self.assertEqual(150, acc_fnds[-2][1])
        self.assertEqual(200, acc_fnds[-1][1])

if __name__ =='__main__':
    unittest.main()
