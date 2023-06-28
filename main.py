import os
import pickle

from cbpro import AuthenticatedClient, PublicClient
from dotenv import load_dotenv
from telegrambot.telegrambot import TelegramBot

def load_default_port_client(dotenv_path: str = '.env') -> AuthenticatedClient:
    load_dotenv(dotenv_path=dotenv_path)

    default_port_passphrase = os.environ['BTC_DCA_DEFAULT_PORTFOLIO_PASSPHRASE']
    default_port_secret_key = os.environ['BTC_DCA_DEFAULT_PORTFOLIO_SECRET_KEY']
    default_port_api_key = os.environ['BTC_DCA_DEFAULT_PORTFOLIO_API_KEY']

    default_port_client = AuthenticatedClient(
        key=default_port_api_key,
        b64secret=default_port_secret_key,
        passphrase=default_port_passphrase
    )

    return default_port_client

def load_btc_bot_client(dotenv_path: str = '.env') -> AuthenticatedClient:

    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.environ['BTC_DCA_API_KEY']
    secret_key = os.environ['BTC_DCA_SECRET_KEY']
    passphrase = os.environ['BTC_DCA_PASSPHRASE']

    auth_client = AuthenticatedClient(
        key=api_key,
        b64secret=secret_key,
        passphrase=passphrase
    )

    return auth_client

def load_telegram_bot(dotenv_path: str = '.env') -> TelegramBot:

    load_dotenv(dotenv_path=dotenv_path)
    bot = TelegramBot(
        chat_id=os.environ['TELEGRAM_BOT_CHAT_ID'],
        bot_token=os.environ['TELEGRAM_BOT_TOKEN']
    )

    return bot


def get_usd_account_balance(client: AuthenticatedClient) -> float:

    accounts = client.get_accounts()
    usd_account = list(filter(lambda x: x['currency'] == 'USD', accounts))[0]
    balance = float(usd_account['balance'])

    return balance

if __name__ == "__main__":
    load_dotenv()

    auth_client = load_btc_bot_client()
    telegram_bot = load_telegram_bot()

    usd_balance = get_usd_account_balance(client=auth_client)

    if usd_balance > 5:
        # We have our auth client, we are going to send in order to buy $5 of bitcoin
        btc_buy_order = auth_client.place_market_order(
            product_id='BTC-USD',
            side='buy',
            funds=5
        )

    else:
        telegram_bot.send_message(
            message="Your account has less than $5 in it. Considering transferring over funds into the account. Thanks!"
        )