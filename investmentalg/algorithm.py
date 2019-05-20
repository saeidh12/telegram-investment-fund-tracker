from .my_db import MyDB
from .portfolio import Portfolio
from .account import Account
from .transactions import Transactions
from .funds import Funds
from .portfolio_fund import PortfolioFund
import matplotlib.pyplot as plt
import numpy as np

class Algorithm(MyDB):
    def __init__(self, db_name, portfolio_id):
        super(Algorithm, self).__init__(db_name)
        self._db_name = db_name
        self._portfolio_id = portfolio_id

    def pay_fees(self):
        prt = Portfolio(self._db_name)
        prt_data = prt.retrieve_id(self._portfolio_id)
        if prt_data[-1] >= 0:
            acc = Account(self._db_name)
            accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
            main_acc = acc.retrieve_id(prt_data[-1])
            for account in accounts:
                if not account[0] == main_acc[0]:
                    if account[4] > 0:
                        self.make_transfer(main_acc[1], account[1], account[4], True)
                    elif account[4] < 0:
                        self.make_transfer(account[1], main_acc[1], np.abs(account[4]), True)
            return acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        return False

    def make_transfer(self, sender_name, reciever_name, amount, force=False):
        if amount < self.portfolio_total_fund and amount > 0:
            amount_perc = amount / self.portfolio_total_fund
            accounts = self.accounts_name_dict
            if amount_perc < accounts[sender_name][2] or force:
                acc = Account(self._db_name)
                acc.update_id(accounts[sender_name][0], percentage=accounts[sender_name][2] - amount_perc)
                acc.update_id(accounts[reciever_name][0], percentage=accounts[reciever_name][2] + amount_perc)

                trs = Transactions(self._db_name)
                trs.create_transaction(-1 * amount, accounts[sender_name][0])
                trs.create_transaction(amount, accounts[reciever_name][0])

                fnd = Funds(self._db_name)
                fnd.create_fund(self.get_account_fund(sender_name), accounts[sender_name][0])
                fnd.create_fund(self.get_account_fund(reciever_name), accounts[reciever_name][0])

                return acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        return False

    @property
    def accounts_name_dict(self):
        accounts_dict = dict()
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
        for account in accounts:
            accounts_dict[account[1]] = account
        return accounts_dict

    def update_total_fund(self, new_fund):
        prt = Portfolio(self._db_name)
        prt_data = prt.retrieve_id(self._portfolio_id)
        acc = Account(self._db_name)
        if prt_data[-1] < 0:
            prt_fund = PortfolioFund(self._db_name)
            prt_fund.create_fund(amount=new_fund, portfolio_fk=self._portfolio_id)
            self._update_all_portfolio_funds()
            return acc.retrieve_accounts_for_portfolio(self._portfolio_id)
        fund_change = new_fund - self.portfolio_total_fund

        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        for account in accounts:
            if not account[0] == prt_data[-1]:
                fund = self.get_account_fund(account[1])
                perc = account[6] if fund_change >= 0 else account[5]
                new_perc = (fund + (account[2] * fund_change * perc)) / new_fund
                acc.update_id(account[0], percentage=new_perc)

        # alt_fund = sum([self.get_account_fund(account.name)[0] for account in self.accounts if not account.name == self.accounts[self.main_account].name])

        l = []
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
        for account in accounts:
            if not account[0] == prt_data[-1]:
                l.append(account[2])
        alt_fund = sum(l)

        acc.update_id(prt_data[-1], percentage=1 - alt_fund)

        prt_fund = PortfolioFund(self._db_name)
        prt_fund.create_fund(amount=new_fund, portfolio_fk=self._portfolio_id)

        self._update_all_portfolio_funds()
        return acc.retrieve_accounts_for_portfolio(self._portfolio_id)

    def _update_all_portfolio_funds(self):
        fnd = Funds(self._db_name)
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        for account in accounts:
            fnd.create_fund(self.get_account_fund(account[1]), account[0])

    @property
    def portfolio_total_fund(self):
        prt_funds = PortfolioFund(self._db_name)
        funds = prt_funds.retrieve_funds_for_portfolio(self._portfolio_id)
        if len(funds) > 0:
            return funds[-1][1]
        return 0.0

    def get_account_fund(self, name):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        for account in accounts:
            if account[1] == name:
                return self.portfolio_total_fund * account[2]
        return False

    def add_account(self, name, fund, fee, risk, profit, is_main=False):

        new_total_fund = self.portfolio_total_fund + fund

        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
        for account in accounts:
            acc_fund = self.get_account_fund(account[1])
            if acc_fund == 0.0:
                acc.update_id(account[0], percentage=0.0)
            else:
                acc.update_id(account[0], percentage=acc_fund / new_total_fund)

        new_account = acc.create_account(name=name, fee=fee, risk=risk, profit=profit, fund_id=self._portfolio_id)
        if fund == 0.0:
            acc.update_id(new_account[0], percentage=0.0)
        else:
            acc.update_id(new_account[0], percentage=fund / new_total_fund)

        prt = Portfolio(self._db_name)

        if is_main:
            prt.update_id(self._portfolio_id, main_account=new_account[0])

        prt_fund = PortfolioFund(self._db_name)
        prt_fund.create_fund(amount=new_total_fund, portfolio_fk=self._portfolio_id)

        fnd = Funds(self._db_name)
        fnd.create_fund(self.get_account_fund(name), new_account[0])

        return acc.retrieve_accounts_for_portfolio(self._portfolio_id)

    def remove_main(self):
        prt = Portfolio(self._db_name)
        prt.update_id(self._portfolio_id, main_account=-1)
        return prt.retrieve_id(self._portfolio_id)

    def make_transaction(self, name, fund):
        if self.get_account_fund(name) + fund >= 0:

            new_total_fund = self.portfolio_total_fund + fund
            acc_id = 'c'
            acc = Account(self._db_name)
            accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
            for account in accounts:
                if account[1] == name:
                    acc_id = account[0]
                    acc.update_id(account[0], percentage=(fund + self.get_account_fund(account[1])) / new_total_fund)
                else:
                    acc.update_id(account[0], percentage=self.get_account_fund(account[1]) / new_total_fund)

            prt_fund = PortfolioFund(self._db_name)
            prt_fund.create_fund(amount=new_total_fund, portfolio_fk=self._portfolio_id)

            trs = Transactions(self._db_name)
            trs.create_transaction(fund, acc_id)

            fnd = Funds(self._db_name)
            fnd.create_fund(self.get_account_fund(name), acc_id)

            return acc.retrieve_accounts_for_portfolio(self._portfolio_id)
            # return self.list_account_transactions(name=name)
        else:
            return False

    def list_my_accounts_funds(self):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        output_str = ''
        for account in accounts:
            fund = self.get_account_fund(account[1])
            output_str += f'{account[1]} (%{account[2] * 100}): {fund}'
            output_str += '\n'
        return output_str

    def list_account_transactions(self, name):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        output_str = ''
        for account in accounts:
            if account[1] == name:
                fund = self.get_account_fund(account[1])

                output_str += f'{account[1]} (%{account[2] * 100}): {fund}'
                output_str += '\n\n'

                trs = Transactions(self._db_name)
                acc_trs = trs.retrieve_transactions_for_account(account[0])
                output_str += '*TRANSACTIONS*\n'
                output_str += '*DATE*\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_|\_\_\_*AMOUNT*\n'
                # output_str += '*DATE*                  |   *AMOUNT*\n'
                for trans in acc_trs:
                    output_str += f'{trans[2]}   |   {trans[1]}'
                    output_str += '\n'
                break
        return output_str

    def list_account_funds(self, name):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        output_str = ''
        for account in accounts:
            if account[1] == name:
                fund = self.get_account_fund(account[1])

                output_str += f'{account[1]} (%{account[2] * 100}): {fund}'
                output_str += '\n\n'

                f = Funds(self._db_name)
                acc_f = f.retrieve_funds_for_account(account[0])
                output_str += 'CHANGES IN FUNDS\n'
                output_str += 'DATE                  |   AMOUNT\n'
                for fi in acc_f:
                    output_str += f'{fi[2]}   |   {fi[1]}'
                    output_str += '\n'
                break
        return output_str

    def chart_portfolio_acounts(self):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)
        x = []
        y = []
        for account in accounts:
            fund = self.get_account_fund(account[1])
            x.append('%s (%0.1f)' % (account[1], fund))
            y.append(account[2])
        plt.close()
        plt.style.use('ggplot')
        plt.axis("equal")
        plt.pie(y, labels=x, autopct='%0.1f%%')
        # plt.show()
        plt.savefig(f'media/portfolio-{self._portfolio_id}-accounts.png', bbox_inches='tight')

    def chart_account_funds(self, name):
        acc = Account(self._db_name)
        accounts = acc.retrieve_accounts_for_portfolio(self._portfolio_id)

        for account in accounts:
            if account[1] == name:
                plt.close()
                plt.style.use('ggplot')
                x = []
                y = []
                f = Funds(self._db_name)
                acc_f = f.retrieve_funds_for_account(account[0])
                for i, fi in enumerate(acc_f):
                    x.append(fi[2])
                    y.append(fi[1])
                plt.plot(x, y)

                # plt.show()
                plt.savefig(f'media/{name}-funds.png', bbox_inches='tight')
                break

    def chart_portfolio_funds(self):
        prt_fund = PortfolioFund(self._db_name)
        funds = prt_fund.retrieve_funds_for_portfolio(portfolio_id=self._portfolio_id)
        plt.close()
        plt.style.use('ggplot')
        x = []
        y = []
        for i, fi in enumerate(funds):
            x.append(fi[2])
            y.append(fi[1])
        plt.plot(x, y)

        # plt.show()
        plt.savefig(f'media/portfolio-{self._portfolio_id}-funds.png', bbox_inches='tight')
