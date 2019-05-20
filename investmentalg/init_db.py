import sqlite3
import os
from .variables import SQL_FILE
from shutil import copyfile


SQL_DIRECTORY = 'investmentalg/databases/'

def backup_db(max_backup):
    root, dirs, files = next(os.walk( SQL_DIRECTORY ))
    db_ids = [int(fl.split('_')[0]) for fl in files]
    max_db_ids = max(db_ids)
    copyfile(f'{SQL_DIRECTORY}{max_db_ids}_{SQL_FILE}', f'{SQL_DIRECTORY}{max_db_ids+1}_{SQL_FILE}')
    if len(files) >= max_backup:
        min_db_ids = min(db_ids)
        os.remove(f'{SQL_DIRECTORY}{min_db_ids}_{SQL_FILE}')
    return f'{SQL_DIRECTORY}{max_db_ids+1}_{SQL_FILE}'

def undo():
    root, dirs, files = next(os.walk( SQL_DIRECTORY ))
    db_ids = [int(fl.split('_')[0]) for fl in files]
    max_db_ids = max(db_ids)
    if len(files) > 1:
        os.remove(f'{SQL_DIRECTORY}{max_db_ids}_{SQL_FILE}')
    root, dirs, files = next(os.walk( SQL_DIRECTORY ))
    db_ids = [int(fl.split('_')[0]) for fl in files]
    max_db_ids = max(db_ids)
    return f'{SQL_DIRECTORY}{max_db_ids}_{SQL_FILE}'

def current_sql_file():
    if not os.path.exists(SQL_DIRECTORY):
        os.makedirs(SQL_DIRECTORY)
    data_files = list()
    root, dirs, files = next(os.walk( SQL_DIRECTORY ))

    if len(files) > 0:
        max_db_ids = max([int(fl.split('_')[0]) for fl in files])
        return f'{SQL_DIRECTORY}{max_db_ids}_{SQL_FILE}'
    else:
        create_db(f'{SQL_DIRECTORY}0_{SQL_FILE}')
        return f'{SQL_DIRECTORY}0_{SQL_FILE}'


def create_db(sql_file):
    if os.path.isfile(sql_file):
        exit(1)

    conn = sqlite3.connect(sql_file)

    c = conn.cursor()



    c.execute('''CREATE TABLE portfolio (
        id                  integer primary key autoincrement,
        MAIN_ACCOUNT_FK     SMALLINT

    )''')


    c.execute('''CREATE TABLE portfolio_funds (
            id          integer primary key autoincrement,
            AMOUNT      FLOAT,
            TIMESTAMP   DATETIME DEFAULT CURRENT_TIMESTAMP,
            PORTFOLIO_FK  SMALLINT
    )''')


    c.execute("""CREATE TABLE account (
            id           integer primary key autoincrement,
            NAME         CHARACTER [(120)] UNIQUE,
            PERCENTAGE   FLOAT,
            TIMESTAMP    DATETIME DEFAULT CURRENT_TIMESTAMP,
            FEE          FLOAT,
            RISK         FLOAT,
            PROFIT       FLOAT,
            PORTFOLIO_FK SMALLINT,
            PASSWORD     CHARACTER [(120)]
    )""")

    c.execute("""CREATE TABLE transactions (
            id          integer primary key autoincrement,
            AMOUNT      FLOAT,
            TIMESTAMP   DATETIME DEFAULT CURRENT_TIMESTAMP,
            ACCOUNT_FK  SMALLINT
    )""")

    c.execute("""CREATE TABLE funds (
            id          integer primary key autoincrement,
            AMOUNT      FLOAT,
            TIMESTAMP   DATETIME DEFAULT CURRENT_TIMESTAMP,
            ACCOUNT_FK  SMALLINT
     )""")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db(f'{SQL_DIRECTORY}0_{SQL_FILE}')
