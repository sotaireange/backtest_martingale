import sys
from pybit.unified_trading import HTTP
import asyncio
import numpy as np
import os
import re



def get_coins_bybit(top):
    session=HTTP()
    info = (session.get_instruments_info(category='spot'))['result']['list'][:top]
    list_tokens=[coin['symbol'] for coin in info]

    return list_tokens


def find_coins_by_timeframe(folder_path, timeframe):
    # Регулярное выражение для поиска совпадений
    pattern = rf".*_(\w+),\s{timeframe}.*\.csv"

    coins = set()  # Используем множество, чтобы избежать дубликатов

    # Поиск файлов в папке
    for filename in os.listdir(folder_path):
        match = re.match(pattern, filename)
        if match:
            coin = match.group(1)  # Извлекаем совпадение для coin
            coins.add(coin)
    return list(coins)




def get_coins(top=1000,folder_path=False,timeframe=False):
    if folder_path:
        coins=find_coins_by_timeframe(folder_path,timeframe)
        print(coins)
    else:
        coins=get_coins_bybit(top)
    return coins