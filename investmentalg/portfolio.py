from .my_db import MyDB

class Portfolio(MyDB):
    def create_portfolio(self):
        cursor = self._db.cursor()
        cursor.execute("INSERT INTO portfolio ( MAIN_ACCOUNT_FK) VALUES (-1)")
        self._db.commit()
        cursor.execute(f"SELECT * FROM portfolio WHERE id = {cursor.lastrowid}")
        return cursor.fetchone()

    def update_id(self, id, main_account):
        cursor = self._db.cursor()
        main_account_str = f"MAIN_ACCOUNT_FK = {main_account}"
        cursor.execute(f"""
            UPDATE portfolio
            SET {main_account_str}
            WHERE id = {id}
        """)
        self._db.commit()
        cursor.execute(f"SELECT * FROM portfolio WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM portfolio WHERE id = {id}")
        return cursor.fetchone()

    def retrieve_portfolios(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM portfolio")
        return cursor.fetchall()

    def delete_id(self, id):
        cursor = self._db.cursor()
        cursor.execute(f"DELETE FROM portfolio WHERE id = {id}")
        self._db.commit()
        return True
