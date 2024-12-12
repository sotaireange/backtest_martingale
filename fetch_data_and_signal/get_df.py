
import logging

import pandas as pd
from datetime import datetime
import os
import re


def get_df_bybit(session,coin,timeframe,limit=1000):
    try:
        klines = session.get_kline(category='spot', symbol=coin, interval=timeframe, limit=limit)['result']['list']
        date_ = []
        open_ = []
        close_ = []
        high_ = []
        low_ = []
        volume_ = []
        for kln in klines[1:]:
            date_.append(datetime.fromtimestamp(int(kln[0]) / 1000))
            open_.append(float(kln[1]))
            high_.append(float(kln[2]))
            low_.append(float(kln[3]))
            close_.append(float(kln[4]))
            volume_.append(float(kln[5]))
        data = pd.DataFrame({'Open': open_, 'High': high_, 'Low': low_, 'Close': close_, 'volume': volume_})
        data.index.name = 'Date'
        data.index = date_
        return data[::-1]
    except Exception as e:
        logging.error(msg=f'{e}\nline 123')
        return False


def find_file_with_coin_and_timeframe(folder_path, coin, timeframe):
    pattern = rf".*_{coin},\s*{timeframe}.*\.csv"
    for filename in os.listdir(folder_path):
        if re.match(pattern, filename):
            return os.path.join(folder_path, filename)

    return None

def get_df_from_path(coin,timeframe,folder_path):
    file_name=find_file_with_coin_and_timeframe(folder_path,coin,timeframe)
    if file_name is None: return False
    df=pd.read_csv(file_name)
    df['time'] = pd.to_datetime(df['time'])
    df['time'] = df['time'].dt.tz_localize(None)
    df.set_index('time',inplace=True)
    df.rename(columns={'time':'Open time','open':'Open','high':'High','low':'Low','close':'Close'},inplace=True)
    return df[20:]

def get_df(client,coin,timeframe,limit,folder_path=False):
    if folder_path:
        df = get_df_from_path(coin,timeframe,folder_path)
    else:
        df= get_df_bybit(client,coin,timeframe,limit)
    return df