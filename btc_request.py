from concurrent.futures import process
import string
from requests import request
import discord
import json
import locale
import requests
import os
from dotenv import load_dotenv

t='test'

url_link = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
load_dotenv()

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def request_helper():
    response_usd = request_btc("USD")
    response_brl = request_btc("BRL")
    mensagem_usd = btc_to_msg(response_usd)
    mensagem_brl = btc_to_msg(response_brl)
    mensagem_discord = msg_to_discord(mensagem_usd, mensagem_brl)
    return(mensagem_discord)

def request_btc(currency):
    payloadParams = {
        'symbol': 'BTC',
        'convert': {currency}
    }

    payloadHeader = {
        'Accepts': 'application/json',
        'Accept-Encoding': 'deflate',
        'X-CMC_PRO_API_KEY': os.getenv('API_COIN_MARKET_CAP'),
    }

    r = requests.get(url_link, headers=payloadHeader, params=payloadParams)
    r = r.json()
    return(r)


def set_brl_or_usd(response):
    if "BRL" in response['data']['BTC']['quote']:
        return "BRL"
    else:
        return "USD"

def set_money_symbol(currency):
    if currency == "BRL":
        return "R$"
    return "U$" 
    
def msg_to_discord(msg_usd, msg_brl):
    mensagem_discord = f"""```
{msg_usd.get_message()[0]}
--------------------------
{msg_brl.get_message()[0]}```
    """
    embend = discord.Embed(title="Bitcoin Ticker", color=msg_brl.get_color(), description=mensagem_discord)
    
    return embend

def btc_to_msg(response):
    btc_helper = btc_request_helpr(response)
    formated = f"""
BTC/{btc_helper.currency}
Preço       {btc_helper.money_symbol} {btc_helper.price()}
1h          {btc_helper.percentage_one_hour()}
24h         {btc_helper.percentage_one_day()}    
7d          {btc_helper.percentage_one_week()}
30d         {btc_helper.percentage_one_month()}
60d         {btc_helper.percentage_two_month()}
90d         {btc_helper.percentage_three_month()}
"""

    formated_class = msg_btc_embend(formated, btc_helper.color_red_green())
    return(formated_class)


class btc_request_helpr():
    def __init__(self, response) -> None:
        self.response = response
        self.currency = set_brl_or_usd(response)     
        self.money_symbol = set_money_symbol(self.currency)
        self.general_info = self.response['data']['BTC']['quote'][self.currency]
        
    def price(self):
        price = self.general_info['price']
        price = self.format_current_price(price)
        return price    
    
    def percentage_one_hour(self):
        percent_hour = self.general_info['percent_change_1h']
        symbol = self.plus_or_menos(percent_hour) 
        percent_hour = self.format_current_price(percent_hour)
        return f"{symbol}{percent_hour}%"
    
    def percentage_one_day(self):
        percent_day = self.general_info['percent_change_24h']
        symbol = self.plus_or_menos(percent_day) 
        percent_day = self.format_current_price(percent_day)
        return f"{symbol}{percent_day}%"
    
    def percentage_one_week(self):
        percent_week = self.general_info['percent_change_7d']
        symbol = self.plus_or_menos(percent_week) 
        percent_week = self.format_current_price(percent_week)
        return f"{symbol}{percent_week}%"
    
    def percentage_one_month(self):
        percent_month = self.general_info['percent_change_30d']
        symbol = self.plus_or_menos(percent_month) 
        percent_month = self.format_current_price(percent_month)
        return f"{symbol}{percent_month}%"
    
    def percentage_two_month(self):
        percent_two_month = self.general_info['percent_change_60d']
        symbol = self.plus_or_menos(percent_two_month) 
        percent_two_month = self.format_current_price(percent_two_month)
        return f"{symbol}{percent_two_month}%"
    
    def percentage_three_month(self):
        percent_three_month = self.general_info['percent_change_90d']
        symbol = self.plus_or_menos(percent_three_month) 
        percent_three_month = self.format_current_price(percent_three_month)
        return f"{symbol}{percent_three_month}%"
    
    def format_current_price(self, value):
        value = locale.currency(value, grouping=True, symbol=None)
        return value
    
    def plus_or_menos(self, value):
        if value >= 0:
            return "▲ +"
        if value < 0:
            return "▼ "
    
    def color_red_green(self):
        value = self.general_info['percent_change_1h']
        if value >= 0:
            return 0x00FF00
        else:
            return 0xFF0000

class msg_btc_embend():
    message = ""
    color = ""
    
    def __init__(self, message: string, color) -> None:
        self.message = message,
        self.color = color
    
    def get_message(self) -> string:
        return self.message
    
    def get_color(self):
        return self.color
