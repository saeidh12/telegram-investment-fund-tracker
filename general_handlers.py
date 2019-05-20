from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler
from investmentalg.init_db import current_sql_file, backup_db, undo

def list_commands(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    reply_str = '''*LIST OF AVAILABLE COMMANDS*\n
    *GENERAL*
    /list_commands
    /undo\n
    *ACCOUNT MANAGEMENT*
    /add_account <name> <fund> <fee> <risk> <profit> <is_main=False>
    /list_accounts
    /chart_accounts
    /edit_account <id> name:<name> fee:<fee> risk:<risk> profit:<profit> password:<password>
    /chart_account_funds <name>\n
    *TRANSACTIONS*
    /make_transaction <name> <fund>
    /make_transfer <sender_name> <reciever_name> <amount(positive)>
    /list_account_transactions <name>\n
    *PORTFOLIO MANAGEMENT*
    /update_total_fund <current_amount>
    /chart_portfolio_funds
    /remove_main
    /set_main <account_id>
    /pay_fees
    /list_portfolios'''

    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=reply_str)#, parse_mode=ParseMode.MARKDOWN)
    except Exception as ex:
        print(ex)

list_commands_handler = CommandHandler('list_commands', list_commands)
start_handler = CommandHandler('start', list_commands)

def undo_prev_change(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    try:
        bot.send_message(chat_id=update.message.chat_id, text=undo())

    except Exception as ex:
        print(ex)

undo_handler = CommandHandler('undo', undo_prev_change)
