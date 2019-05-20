from .my_db import MyDB


class Funds(MyDB):
    def create_fund(self, amount, account_fk):
        fund = self._db.cursor()
        fund.execute(f"INSERT INTO funds (amount, account_fk) VALUES ({amount}, {account_fk})")
        self._db.commit()

        fund.execute(f"SELECT * FROM funds WHERE id = {fund.lastrowid}")
        return fund.fetchone()


    def update_id(self, id, amount=None, account_fk=None):
        cursor = self._db.cursor()

        amount_str = f"AMOUNT = '{amount}'" if not amount == None else ""
        sep0 = ',' if not amount == None and account_fk else ' '
        account_fk_str = f"ACCOUNT_FK = {account_fk}" if account_fk else ""


        cursor.execute(f"""
                    UPDATE funds
                    SET {amount_str}{sep0}{account_fk_str}
                    WHERE id = {id}
                """)

        self._db.commit()
        cursor.execute(f"SELECT * FROM funds WHERE id = {id}")
        return cursor.fetchone()

    def delete_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"DELETE FROM funds WHERE id = {id}")
        self._db.commit()
        return True

    def retrieve_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM funds WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_funds(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM funds")
        return cursor.fetchall()

    def retrieve_funds_for_account(self, account_id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM funds WHERE account_fk = {account_id}")
        return cursor.fetchall()
