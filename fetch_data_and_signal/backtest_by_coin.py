import os
import csv
import logging
from pybit.unified_trading import HTTP
from .get_coins import get_coins
from .get_df import get_df
from .backtest import backtest_coin
from .utils import *


async def backtest_coin_with_param(data):
    indicator='martingale'
    fieldnames=get_fieldnames(indicator)
    data_signal=get_data_signal(data,indicator)
    timeframe=data[indicator].get('by_coin').get('timeframe')
    top=data[indicator].get('params',{}).get('top',100)

    folder_path=use_folder_path(data)

    folder_path_result=f'coins'

    if not os.path.exists(folder_path_result):
        os.makedirs(folder_path_result,exist_ok=True)

    file_name=get_file_or_patch_name(data_signal,timeframe,indicator)
    file_path = os.path.join(folder_path_result, file_name)

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    coins=get_coins(top,folder_path,timeframe)

    client=HTTP()



    logging.info(f'Начало сбора, параметры:\n{data[indicator]['by_coin']}')
    rows=[]

    for i,coin in enumerate(coins):
        df=get_df(client,coin,timeframe,data['limit'],folder_path)
        try:
            res=backtest_coin(df,data_signal)


            row = get_row(coin,timeframe,data_signal,res,indicator)
            rows.append(row)
        except Exception as e:
            logging.error(f'Exception occurred {e}',exc_info=True)


    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(rows)