from telegram.ext import Updater
import logging
from variables_and_functions import CONFIG_FILE, read_from_config_file

from account_handlers import add_account_handler, list_accounts_handler, chart_accounts_handler, edit_account_handler, chart_account_funds_handler
from transaction_handlers import make_transaction_handler, make_transfer_handler, list_account_transactions_handler
from portfolio_handlers import update_total_fund_handler, chart_portfolio_funds_handler, remove_main_handler, set_main_handler, pay_fees_handler, list_portfolios_handler
from general_handlers import list_commands_handler, start_handler, undo_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(read_from_config_file(CONFIG_FILE, 'creds', 'token'))

updater.dispatcher.add_handler(add_account_handler)
updater.dispatcher.add_handler(list_accounts_handler)
updater.dispatcher.add_handler(chart_accounts_handler)
updater.dispatcher.add_handler(edit_account_handler)
updater.dispatcher.add_handler(chart_account_funds_handler)

updater.dispatcher.add_handler(make_transaction_handler)
updater.dispatcher.add_handler(make_transfer_handler)
updater.dispatcher.add_handler(list_account_transactions_handler)

updater.dispatcher.add_handler(update_total_fund_handler)
updater.dispatcher.add_handler(chart_portfolio_funds_handler)
updater.dispatcher.add_handler(remove_main_handler)
updater.dispatcher.add_handler(set_main_handler)
updater.dispatcher.add_handler(pay_fees_handler)
updater.dispatcher.add_handler(list_portfolios_handler)

updater.dispatcher.add_handler(list_commands_handler)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(undo_handler)

updater.start_polling()
updater.idle()
