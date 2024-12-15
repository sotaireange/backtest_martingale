import json
import pandas as pd


def get_keys(indicator):
    if indicator=='martingale':
        keys=['start_position_size', 'takeprofit', 'start_martingale_percent', 'martingale_multiplayer','bb_deviation']
    elif indicator=='martingale_mult':
        keys =['start_position_size', 'takeprofit', 'start_martingale_percent', 'martingale_multiplayer','bb_deviation','correction_buy_mult','takeprofit_mult']
    return keys


def get_matching_rows(df_filtered,row,indicator='martingale',coin=False):
    if indicator=='martingale':
        matching_rows = df_filtered[
            (df_filtered['start_position_size'] == row['start_position_size']) &
            (df_filtered['takeprofit'] == row['takeprofit']) &
            (df_filtered['start_martingale_percent'] == row['start_martingale_percent']) &
            (df_filtered['martingale_multiplayer'] == row['martingale_multiplayer']) &
            (df_filtered['bb_deviation'] == row['bb_deviation']) &
            ((df_filtered['coin'] != row['coin']) if coin else True)
            ]
    elif indicator=='martingale':
        matching_rows = df_filtered[
            (df_filtered['start_position_size'] == row['start_position_size']) &
            (df_filtered['takeprofit'] == row['takeprofit']) &
            (df_filtered['start_martingale_percent'] == row['start_martingale_percent']) &
            (df_filtered['martingale_multiplayer'] == row['martingale_multiplayer']) &
            (df_filtered['bb_deviation'] == row['bb_deviation']) &
            (df_filtered['correction_buy_mult'] == row['correction_buy_mult']) &
            (df_filtered['takeprofit_mult'] == row['takeprofit_mult']) &
            ((df_filtered['coin'] != row['coin']) if coin else True)
            ]

    return matching_rows



def profit_by_coin(df: pd.DataFrame,indicator):
    best_keys = df.loc[df.groupby('coin')['pnl'].idxmax()]
    keys=get_keys(indicator)
    result = best_keys[keys].copy()
    result['moneydown'] = 0.0
    result['won'] = 0
    result['pnl'] = 0
    result['pnl_perc'] = 0.0
    result['pnl_average'] = 0
    result['pnl_average_perc'] = 0
    result['len_total'] = 0.0
    result['len_average'] = 0
    result['len_max'] = 0
    result['n'] = 0
    keys=['coin']+keys+['moneydown', 'won', 'pnl','pnl_perc','pnl_average','pnl_average_perc','len_total','len_average','len_max']
    df_filtered = df[keys]

    for idx, row in best_keys.iterrows():
        matching_rows =  get_matching_rows(df_filtered, row,indicator,coin=True)

        if not matching_rows.empty:
            result.loc[idx, 'moneydown'] = int(matching_rows['moneydown'].sum())
            result.loc[idx, 'won'] = int(matching_rows['won'].sum())
            result.loc[idx, 'pnl'] = int(matching_rows['pnl'].sum())
            result.loc[idx, 'pnl_perc'] = int(matching_rows['pnl_perc'].sum())
            result.loc[idx, 'pnl_average'] = int(matching_rows['pnl_average'].sum())
            result.loc[idx, 'pnl_average_perc'] = int(matching_rows['pnl_average_perc'].sum())
            result.loc[idx, 'len_total'] = int(matching_rows['len_total'].sum())
            result.loc[idx, 'len_average'] = int(matching_rows['len_average'].sum())
            result.loc[idx, 'len_max'] = int(matching_rows['len_max'].sum())
            result.loc[idx, 'n'] = matching_rows.shape[0]

    return result



def profit_by_coin_using_signals(df: pd.DataFrame, signals: list,indicator):
    result = pd.DataFrame(signals)
    result['moneydown'] = 0.0
    result['won'] = 0
    result['pnl'] = 0
    result['pnl_perc'] = 0.0
    result['pnl_average'] = 0
    result['pnl_average_perc'] = 0
    result['len_total'] = 0.0
    result['len_average'] = 0
    result['len_max'] = 0
    result['n'] = 0
    keys=get_keys(indicator)
    keys=['coin']+keys+['moneydown', 'won', 'pnl','pnl_perc','pnl_average','pnl_average_perc','len_total','len_average','len_max']
    df_filtered = df[keys]
    for idx, signal in enumerate(signals):
        matching_rows = get_matching_rows(df_filtered,signal,indicator)

        if not matching_rows.empty:
            result.loc[idx, 'moneydown'] = int(matching_rows['moneydown'].sum())
            result.loc[idx, 'won'] = int(matching_rows['won'].sum())
            result.loc[idx, 'pnl'] = int(matching_rows['pnl'].sum())
            result.loc[idx, 'pnl_perc'] = int(matching_rows['pnl_perc'].sum())
            result.loc[idx, 'pnl_average'] = int(matching_rows['pnl_average'].sum())
            result.loc[idx, 'pnl_average_perc'] = int(matching_rows['pnl_average_perc'].sum())
            result.loc[idx, 'len_total'] = int(matching_rows['len_total'].sum())
            result.loc[idx, 'len_average'] = int(matching_rows['len_average'].sum())
            result.loc[idx, 'len_max'] = int(matching_rows['len_max'].sum())
            result.loc[idx, 'n'] = matching_rows.shape[0]

    return result



def analyze_parameters(df: pd.DataFrame, parameter: str,indicator):
    analysis_result = df.groupby(parameter).agg({
        'moneydown': 'mean',
        'won': 'mean',
        'pnl': 'mean',
        'pnl_perc': 'mean',
        'pnl_average': 'mean',
        'pnl_average_perc': 'mean',
        'len_total': 'mean',
        'len_average': 'mean',
        'len_max': 'mean',
    }).reset_index()

    analysis_result.columns = [parameter, 'avg_moneydown', 'avg_won', 'avg_pnl','avg_pnl_perc',
                               'avg_pnl_average','avg_pnl_average_perc','avg_len_total','avg_len_average','avg_len_max']

    return analysis_result


