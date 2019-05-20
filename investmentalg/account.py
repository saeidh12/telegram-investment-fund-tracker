from .my_db import MyDB
import random

class Account(MyDB):

    def create_account(self, name, fee, risk, profit, fund_id):
        acc = self._db.cursor()
        acc.execute(f"INSERT INTO account (name, percentage, fee, risk, profit, PORTFOLIO_FK, PASSWORD) VALUES ('{name}', 0, {fee}, {risk}, {profit}, {fund_id}, {str(random.randint(100000,1000000))})")
        self._db.commit()
        acc.execute(f"SELECT * FROM account WHERE id = {acc.lastrowid}")
        return acc.fetchone()


    def update_id(self, id, name=None, percentage=None, fee=None, risk=None, profit=None, fund_fk=None, password=None):
        cursor = self._db.cursor()

        name_str = f"NAME = '{name}'" if name else ""
        sep0 = ',' if name and not percentage == None else ' '

        percentage_str = f"PERCENTAGE = {percentage}" if not percentage == None else " "
        sep1 = ',' if (name or not percentage == None) and not fee == None else ' '

        fee_str = f"FEE = {fee}" if not fee == None else ""
        sep2 = ',' if (name or not percentage == None or not fee == None) and not risk == None else ' '

        risk_str = f"RISK = {risk}" if not risk == None else ""
        sep3 = ',' if (name or not percentage == None or not fee == None or not risk == None) and not profit == None else ' '

        profit_str = f"PROFIT = {profit}" if not profit == None else ""
        sep4 = ',' if (name or not percentage == None or not fee == None or not risk == None or not profit == None ) and not fund_fk == None else ' '

        fund_fk_str = f"PORTFOLIO_FK = {fund_fk}" if fund_fk else ""
        sep5 = ',' if (name or not percentage == None or not fee == None or not risk == None or not profit == None or not fund_fk == None ) and not password == None else ' '

        password_str = f"PASSWORD = {password}" if password else ""

        cursor.execute(f"""
                    UPDATE account
                    SET {name_str}{sep0}{percentage_str}{sep1}{fee_str}{sep2}{risk_str}{sep3}{profit_str}{sep4}{fund_fk_str}{sep5}{password_str}
                    WHERE id = {id}
                """)

        self._db.commit()
        cursor.execute(f"SELECT * FROM account WHERE id = {id}")
        return cursor.fetchone()

    def delete_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"DELETE FROM account WHERE id = {id}")
        self._db.commit()
        return True


    def retrieve_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM account WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_accounts(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM account")
        return cursor.fetchall()

    def retrieve_accounts_for_portfolio(self, portfolio_id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM account WHERE PORTFOLIO_FK = {portfolio_id}")
        return cursor.fetchall()
