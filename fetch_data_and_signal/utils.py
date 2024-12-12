
def get_fieldnames(indicator):
    if indicator == 'martingale':
        fieldnames = ['coin', 'timeframe', 'start_position_size',
                      'takeprofit','start_martingale_percent','martingale_multiplayer','bb_deviation',
                      'moneydown','won', 'pnl', 'pnl_perc','pnl_average',
                      'pnl_average_perc','len_total', 'len_average', 'len_max']
        return fieldnames

def get_data_signal(data,indicator):
    if indicator=='martingale':
        data_signal={
            'start_position_size': data.get(indicator,{}).get('by_coin').get('start_position_size'),
            'takeprofit': data.get(indicator,{}).get('by_coin').get('takeprofit'),
            'start_martingale_percent': data.get(indicator,{}).get('by_coin').get('start_martingale_percent'),
            'martingale_multiplayer': data.get(indicator,{}).get('by_coin').get('martingale_multiplayer'),
            'bb_deviation': data.get(indicator,{}).get('by_coin').get('bb_deviation'),

        }
        return data_signal

def get_file_or_patch_name(data_signal,timeframe,indicator,stock=False):
    if indicator=='martingale':
        if stock:
            file_name=(f'S_{data_signal["start_position_size"][0]}_{data_signal["start_position_size"][-1]}_T_{data_signal["takeprofit"][0]}'
                       f'_{data_signal["takeprofit"][-1]}_P_{data_signal["start_martingale_percent"][0]}_{data_signal["start_martingale_percent"][-1]}'
                       f'_M_{round(data_signal["martingale_multiplayer"][0],2)}_{round(data_signal["martingale_multiplayer"][-1],2)}'
                       f'_D_{data_signal["bb_deviation"][0]}_{data_signal["bb_deviation"][-1]}'
                       f'_T_{timeframe}_{indicator}')

        else:
            file_name = (f'S_{data_signal["start_position_size"]}_T_{data_signal["takeprofit"]}_P_{data_signal["start_martingale_percent"]}'
                         f'_M_{data_signal["martingale_multiplayer"]}_D_{data_signal["bb_deviation"]}_T_{timeframe}_{indicator}.csv')
        return file_name


def get_row(coin,timeframe,data_signal,res,indicator):
    if indicator=='martingale':
        row = {
            'coin': coin,
            'timeframe': timeframe,
            'start_position_size':data_signal['start_position_size'],
            'takeprofit': data_signal['takeprofit'],
            'start_martingale_percent':data_signal['start_martingale_percent'],
            'martingale_multiplayer':round(data_signal['martingale_multiplayer'],2),
            'bb_deviation': float(data_signal['bb_deviation']),
            'moneydown': float(res.get('moneydown',0)),
            'won': float(res.get('won',0)),
            'pnl': float(res.get('pnl',0)),
            'pnl_perc': float(res.get('pnl_perc',0)),
            'pnl_average': float(res.get('pnl_average',0)),
            'pnl_average_perc': float(res.get('pnl_average_perc',0)),
            'len_total': float(res.get('len_total',0)),
            'len_average': float(res.get('len_average',0)),
            'len_max': float(res.get('len_max',0)),

        }
        return row


def use_folder_path(data):
    use_folder=data['use_folder']
    if use_folder:
        folder_path=data['folder_path']
    else:
        folder_path=False
    return folder_path