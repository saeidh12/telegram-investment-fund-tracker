from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler
from investmentalg.algorithm import Algorithm
from investmentalg.init_db import current_sql_file, backup_db
from variables_and_functions import CONFIG_FILE, read_from_config_file

def make_transaction(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if not len(args) == 2:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/make_transaction <name> <fund>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
            alg.make_transaction(name=args[0], fund=float(args[1]))
            transaction_list = alg.list_account_transactions(name=args[0])

            bot.send_message(chat_id=update.message.chat_id,
                             text=transaction_list, parse_mode=ParseMode.MARKDOWN)
        except Exception as ex:
            print(ex)

make_transaction_handler = CommandHandler('make_transaction', make_transaction, pass_args=True)

def make_transfer(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if not len(args) == 3:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/make_transfer <sender_name> <reciever_name> <amount(positive)>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            prt_id = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
            alg = Algorithm(current_sql_file(), prt_id)
            alg.make_transfer(sender_name=args[0], reciever_name=args[1], amount=float(args[2]))
            alg.chart_portfolio_acounts()

            bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(f'media/portfolio-{prt_id}-accounts.png', 'rb'))
        except Exception as ex:
            print(ex)

make_transfer_handler = CommandHandler('make_transfer', make_transfer, pass_args=True)

def list_account_transactions(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if not len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/list_account_transactions <name>")

    else:
        try:
            alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
            transaction_list = alg.list_account_transactions(name=args[0])

            bot.send_message(chat_id=update.message.chat_id,
                             text=transaction_list, parse_mode=ParseMode.MARKDOWN)
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
        except Exception as ex:
            print(ex)

list_account_transactions_handler = CommandHandler('list_account_transactions', list_account_transactions, pass_args=True)
