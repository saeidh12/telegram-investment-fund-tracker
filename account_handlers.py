from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler
from investmentalg.algorithm import Algorithm
from investmentalg.account import Account
from investmentalg.init_db import current_sql_file, backup_db
from variables_and_functions import CONFIG_FILE, read_from_config_file

def add_account(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if len(args) < 5:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/add_account <name> <fund> <fee> <risk> <profit> <is_main=False>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
            accounts = alg.add_account(name=args[0], fund=float(args[1]), fee=float(args[2]), risk=float(args[3]), profit=float(args[4]), is_main=bool(args[5]) if len(args) == 6 else False)
            reply_str = str()
            for account in accounts:
                if account[1] == args[0]:
                    reply_str += f'ID: *{account[0]}*' + '\n'
                    reply_str += f'NAME: *{account[1]}*' + '\n'
                    reply_str += f'PERCENTAGE: *{account[2]*100}*' + '\n'
                    reply_str += f'FEE: *{account[4]}*' + '\n'
                    reply_str += f'RISK: *{account[5]*100}*' + '\n'
                    reply_str += f'PROFIT: *{account[6]*100}*' + '\n'
                    reply_str += f'TIMESTAMP: {account[3]}' + '\n'

            bot.send_message(chat_id=update.message.chat_id,
                             text=reply_str, parse_mode=ParseMode.MARKDOWN)
        except Exception as ex:
            print(ex)

add_account_handler = CommandHandler('add_account', add_account, pass_args=True)


def list_accounts(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)

    try:
        acc = Account(current_sql_file())
        accounts = acc.retrieve_accounts_for_portfolio(read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
        reply_str = '*ACCOUNTS*\n\n'
        for account in accounts:
            reply_str += f'ID: *{account[0]}*' + '\n'
            reply_str += f'NAME: *{account[1]}*' + '\n'
            reply_str += f'PERCENTAGE: *{account[2]*100}*' + '\n'
            reply_str += f'FEE: *{account[4]}*' + '\n'
            reply_str += f'RISK: *{account[5]*100}*' + '\n'
            reply_str += f'PROFIT: *{account[6]*100}*' + '\n'
            reply_str += f'TIMESTAMP: {account[3]}' + '\n\n'

        bot.send_message(chat_id=update.message.chat_id,
                         text=reply_str, parse_mode=ParseMode.MARKDOWN)
    except Exception as ex:
        print(ex)

list_accounts_handler = CommandHandler('list_accounts', list_accounts)


def chart_accounts(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)

    try:
        alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
        alg.chart_portfolio_acounts()

        prt = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(f'media/portfolio-{prt}-accounts.png', 'rb'))
    except Exception as ex:
        print(ex)

chart_accounts_handler = CommandHandler('chart_accounts', chart_accounts)


def edit_account(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if len(args) < 2 or len(args) > 6:
        bot.send_message(chat_id=update.message.chat_id,
                         text="/edit_account <id> name:<name> fee:<fee> risk:<risk> profit:<profit> password:<password>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            acc = Account(current_sql_file())
            params = dict()
            for arg in args[1:]:
                param = arg.split(':')
                params[param[0]] = param[1]

            account = acc.update_id(id=args[0], **params)
            reply_str = str()
            reply_str += f'ID: *{account[0]}*' + '\n'
            reply_str += f'NAME: *{account[1]}*' + '\n'
            reply_str += f'PERCENTAGE: *{account[2]*100}*' + '\n'
            reply_str += f'FEE: *{account[4]}*' + '\n'
            reply_str += f'RISK: *{account[5]*100}*' + '\n'
            reply_str += f'PROFIT: *{account[6]*100}*' + '\n'
            reply_str += f'TIMESTAMP: {account[3]}' + '\n'

            bot.send_message(chat_id=update.message.chat_id,
                             text=reply_str, parse_mode=ParseMode.MARKDOWN)
        except Exception as ex:
            print(ex)

edit_account_handler = CommandHandler('edit_account', edit_account, pass_args=True)

def chart_account_funds(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)

    if not len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="/chart_account_funds <name>")
    else:
        try:
            alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
            alg.chart_account_funds(name=args[0])

            bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(f'media/{args[0]}-funds.png', 'rb'))
        except Exception as ex:
            print(ex)

chart_account_funds_handler = CommandHandler('chart_account_funds', chart_account_funds, pass_args=True)
