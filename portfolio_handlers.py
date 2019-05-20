from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler
from investmentalg.algorithm import Algorithm
from investmentalg.portfolio import Portfolio
from investmentalg.init_db import current_sql_file, backup_db
from variables_and_functions import CONFIG_FILE, read_from_config_file

def update_total_fund(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if not len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/update_total_fund <current_amount>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
            alg.update_total_fund(new_fund=float(args[0]))
            alg.chart_portfolio_funds()

            prt = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
            bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(f'media/portfolio-{prt}-funds.png', 'rb'))
        except Exception as ex:
            print(ex)

update_total_fund_handler = CommandHandler('update_total_fund', update_total_fund, pass_args=True)

def chart_portfolio_funds(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    try:
        prt = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
        alg = Algorithm(current_sql_file(), prt)
        alg.chart_portfolio_funds()

        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(f'media/portfolio-{prt}-funds.png', 'rb'))
    except Exception as ex:
        print(ex)

chart_portfolio_funds_handler = CommandHandler('chart_portfolio_funds', chart_portfolio_funds)

def remove_main(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    try:
        backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
        alg = Algorithm(current_sql_file(), read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id'))
        prt = alg.remove_main()

        reply_str = str()
        reply_str += f'ID: *{prt[0]}*' + '\n'
        reply_str += f'MAIN\_ACCOUNT\_FK: *{prt[1]}*'

        bot.send_message(chat_id=update.message.chat_id,
                         text=reply_str, parse_mode=ParseMode.MARKDOWN)
    except Exception as ex:
        print(ex)

remove_main_handler = CommandHandler('remove_main', remove_main)

def set_main(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    if not len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                                 text="/set_main <account_id>")

    else:
        try:
            backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
            prt = Portfolio(current_sql_file())
            prt_id = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
            prt.update_id(prt_id, main_account=int(args[0]))
            prt = prt.retrieve_id(prt_id)

            reply_str = str()
            reply_str += f'ID: *{prt[0]}*' + '\n'
            reply_str += f'MAIN\_ACCOUNT\_FK: *{prt[1]}*'

            bot.send_message(chat_id=update.message.chat_id,
                             text=reply_str, parse_mode=ParseMode.MARKDOWN)
        except Exception as ex:
            print(ex)

set_main_handler = CommandHandler('set_main', set_main, pass_args=True)

def pay_fees(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    try:
        backup_db(max_backup=int(read_from_config_file(CONFIG_FILE, 'creds', 'num_backup_dbs')))
        prt_id = read_from_config_file(CONFIG_FILE, 'creds', 'portfolio_id')
        alg = Algorithm(current_sql_file(), prt_id)
        alg.pay_fees()

        alg.chart_portfolio_acounts()

        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(f'media/portfolio-{prt_id}-accounts.png', 'rb'))
    except Exception as ex:
        print(ex)

pay_fees_handler = CommandHandler('pay_fees', pay_fees)

def list_portfolios(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    try:
        p = Portfolio(current_sql_file())
        prts = p.retrieve_portfolios()

        reply_str = str()
        for prt in prts:
            reply_str += f'ID: *{prt[0]}*' + '\n'
            reply_str += f'MAIN\_ACCOUNT\_FK: *{prt[1]}*\n\n'

        bot.send_message(chat_id=update.message.chat_id,
                         text=reply_str, parse_mode=ParseMode.MARKDOWN)
    except Exception as ex:
        print(ex)

list_portfolios_handler = CommandHandler('list_portfolios', list_portfolios)
