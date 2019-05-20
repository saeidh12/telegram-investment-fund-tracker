from .my_db import MyDB

class Transactions(MyDB):
    def create_transaction(self, amount, account_fk):
        trs = self._db.cursor()
        trs.execute(f"INSERT INTO transactions (amount, account_fk) VALUES ({amount}, {account_fk})")
        self._db.commit()

        trs.execute(f"SELECT * FROM transactions WHERE id = {trs.lastrowid}")
        return trs.fetchone()


    def update_id(self, id, amount=None, account_fk=None):
        cursor = self._db.cursor()

        amount_str = f"AMOUNT = '{amount}'" if not amount == None else ""
        sep0 = ',' if not amount == None and account_fk else ' '
        account_fk_str = f"ACCOUNT_FK = {account_fk}" if account_fk else ""


        cursor.execute(f"""
                    UPDATE transactions
                    SET {amount_str}{sep0}{account_fk_str}
                    WHERE id = {id}
                """)

        self._db.commit()
        cursor.execute(f"SELECT * FROM transactions WHERE id = {id}")
        return cursor.fetchone()

    def delete_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"DELETE FROM transactions WHERE id = {id}")
        self._db.commit()
        return True

    def retrieve_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM transactions WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_transactions(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()

    def retrieve_transactions_for_account(self, account_id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM transactions WHERE account_fk = {account_id}")
        return cursor.fetchall()
