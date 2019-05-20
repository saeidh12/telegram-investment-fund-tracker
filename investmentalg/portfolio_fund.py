from .my_db import MyDB

class PortfolioFund(MyDB):
    def create_fund(self, amount, portfolio_fk):
        trs = self._db.cursor()
        trs.execute(f"INSERT INTO portfolio_funds (amount, portfolio_fk) VALUES ({amount}, {portfolio_fk})")
        self._db.commit()

        trs.execute(f"SELECT * FROM portfolio_funds WHERE id = {trs.lastrowid}")
        return trs.fetchone()


    def update_id(self, id, amount=None, portfolio_fk=None):
        cursor = self._db.cursor()

        amount_str = f"AMOUNT = '{amount}'" if not amount == None else ""
        sep0 = ',' if not amount == None and portfolio_fk else ' '
        portfolio_fk_str = f"PORTFOLIO_FK = {portfolio_fk}" if portfolio_fk else ""


        cursor.execute(f"""
                    UPDATE portfolio_funds
                    SET {amount_str}{sep0}{portfolio_fk_str}
                    WHERE id = {id}
                """)

        self._db.commit()
        cursor.execute(f"SELECT * FROM portfolio_funds WHERE id = {id}")
        return cursor.fetchone()

    def delete_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"DELETE FROM portfolio_funds WHERE id = {id}")
        self._db.commit()
        return True

    def retrieve_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM portfolio_funds WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_portfolio(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM portfolio_funds")
        return cursor.fetchall()

    def retrieve_funds_for_portfolio(self, portfolio_id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM portfolio_funds WHERE portfolio_fk = {portfolio_id}")
        return cursor.fetchall()
