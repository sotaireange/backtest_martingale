import itertools
import numpy as np
def get_data_for_signal(data,only_params=False,indicator='martingale'):
    if indicator=='martingale':
        parameters = {
            'start_position_size': range(data[indicator]['params']['start_position_size']['min'], data[indicator]['params']['start_position_size']['max']+1),        # lenght: от 1 до 10
            'takeprofit': range(data[indicator]['params']['takeprofit']['min'],data[indicator]['params']['takeprofit']['max']+1),     # len_signal: от 3 до 6 мб 3-6
            'start_martingale_percent': range(data[indicator]['params']['start_martingale_percent']['min'],data[indicator]['params']['start_martingale_percent']['max']+1),           # atr: думаю лучше 3
            'martingale_multiplayer': np.arange(data[indicator]['params']['martingale_multiplayer']['min'],data[indicator]['params']['martingale_multiplayer']['max']+0.1,0.1)[0:-1],
            'bb_deviation': range(data[indicator]['params']['bb_deviation']['min'],data[indicator]['params']['bb_deviation']['max']+1)           # atr: думаю лучше 3

        }
    elif indicator=='martingale_adv':
        parameters = {
            'start_position_size': range(data[indicator]['params']['start_position_size']['min'], data[indicator]['params']['start_position_size']['max']+1),        # lenght: от 1 до 10
            'takeprofit': range(data[indicator]['params']['takeprofit']['min'],data[indicator]['params']['takeprofit']['max']+1),     # len_signal: от 3 до 6 мб 3-6
            'start_martingale_percent': range(data[indicator]['params']['start_martingale_percent']['min'],data[indicator]['params']['start_martingale_percent']['max']+1),           # atr: думаю лучше 3
            'martingale_multiplayer': np.arange(data[indicator]['params']['martingale_multiplayer']['min'],data[indicator]['params']['martingale_multiplayer']['max']+0.1,0.1)[0:-1],
            'bb_deviation': range(data[indicator]['params']['bb_deviation']['min'],data[indicator]['params']['bb_deviation']['max']+1),
            'correction_buy_mult': np.arange(data[indicator]['params']['correction_buy_mult']['min'],data[indicator]['params']['correction_buy_mult']['max']+0.1,0.1)[0:-1],
            'takeprofit_mult': np.arange(data[indicator]['params']['takeprofit_mult']['min'],data[indicator]['params']['takeprofit_mult']['max']+0.1,0.1)[0:-1]
        }

        if only_params: return parameters
    combinations = list(itertools.product(*parameters.values()))
    data_for_signal_list = [dict(zip(parameters.keys(), combination)) for combination in combinations]
    return data_for_signal_list