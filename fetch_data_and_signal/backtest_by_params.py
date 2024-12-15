import os
import csv
import logging
from pybit.unified_trading import HTTP
import asyncio
import concurrent.futures
import json
import pandas as pd
import numpy as np
import time
logging.basicConfig(level=logging.INFO)

from .get_combinations_params import get_data_for_signal
from .get_coins import get_coins
from .get_df import get_df
from .backtest import backtest
from .utils import *

def iter_coin_by_params(coins,client,timeframe,data_signals,data,file_path,fieldnames,indicator,folder_path):
    try:
        time.sleep(np.random.randint(1,3))
        for i,coin in enumerate(coins):
            df=get_df(client,coin,timeframe,data['limit'],folder_path)
            rows=[]
            for data_signal in data_signals:
                try:
                    res=backtest(df,data_signal,indicator)
                    row = get_row(coin,timeframe,data_signal,res,indicator)
                    rows.append(row)
                except Exception as e:
                    logging.error(f'error {coin}\n{data_signal}\n{e}',exc_info=True)

            with open(file_path, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerows(rows)

            logging.info(f'{coin} is finish {i+1}/{len(coins)}')
    except Exception as e:
        logging.error(f'Main error {e}',exc_info=True)



async def backtest_coins_by_params(data): #TODO: Гдето тут нужно исправитть чтобы использовать folder
    try:
        indicator=data['indicator']
        fieldnames=get_fieldnames(indicator)
        timeframe=data[indicator].get('params',{}).get('timeframe',30)
        top=data[indicator].get('params',{}).get('top',100)

        folder_path=use_folder_path(data)
        params=get_data_for_signal(data,only_params=True,indicator=indicator)
        folder_path_result=get_file_or_patch_name(params,timeframe,indicator,stock=True)
        if not os.path.exists(folder_path_result):
            os.makedirs(folder_path_result,exist_ok=True)

        file_path = os.path.join(folder_path_result, 'results_coins.csv')


        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

        print(f'Сбор монеток')
        coins=get_coins(top,folder_path,timeframe)
        print(f'Найдено монеток {len(coins)}')

        df=pd.read_csv(file_path,low_memory=False)

        if not df.empty:
            coins_already=df['coin'].unique().tolist()
            coins=list(set(coins)-set(coins_already))

        client=HTTP()

        data_signals=get_data_for_signal(data,indicator=indicator)
        logging.info(msg=f'Начало сбора, параметры:\n{data[indicator].get('params',{})}\n'
                         f'Кол-во Монет {len(coins)}')

        num_processes = data.get('core',10)
        coin_chunks = np.array_split(coins, num_processes)
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
                futures = [
                    executor.submit(iter_coin_by_params, chunk, client, timeframe, data_signals, data, file_path, fieldnames,indicator,folder_path)
                    for chunk in coin_chunks
                ]
        except Exception as e:
            logging.error(f"ERROR WHEN CREATE MULTIPROC {e}")
        logging.info(f'Конец сбора')
    except Exception as e:
        logging.error(f"ERROR FULL {e}",exc_info=True)


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        data=json.load(f)
    asyncio.run(backtest_coins_by_params(data))
