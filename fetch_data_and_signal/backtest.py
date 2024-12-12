
import backtrader as bt
import math

class MartingaleStrategy(bt.Strategy):
    params = (
        ('start_position_size', 10.0),
        ('take_profit_percent', 15.0),
        ('martingale_percent', 3.0),
        ('martingale_mult', 2.0),
        ('rsi_length', 14),
        ('rsi_bb_length', 20),
        ('price_bb_length', 20),
        ('deviation', 2.0),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_length)
        self.bb_rsi = bt.indicators.BollingerBands(self.rsi, period=self.params.rsi_bb_length, devfactor=self.params.deviation)
        self.bb_price = bt.indicators.BollingerBands(self.data.close, period=self.params.price_bb_length, devfactor=self.params.deviation)

        self.first_buy_price = None
        self.last_buy_price = None
        self.count_martingale = 0
        self.start_unit_size = 0

    def next(self):
        equity = self.broker.get_value()
        unit_size = equity * (self.params.start_position_size / 100) / self.data.close[0]

        if not self.position:
            if self.rsi[0] < self.bb_rsi.lines.bot[0] and self.data.close[0] < self.bb_price.lines.bot[0]:
                self.buy(size=unit_size)
                self.first_buy_price = self.data.close[0]
                self.last_buy_price = self.data.close[0]
                self.count_martingale = 1
        else:
            price_percent = (self.data.close[0] - self.position.price) * 100 / self.position.price

            if price_percent >= self.params.take_profit_percent:
                self.close()
                self.first_buy_price = None
                self.last_buy_price = None
                self.count_martingale = 0
                return

            next_buy_price = self.first_buy_price * (1 - (self.params.martingale_percent / 100) * self.count_martingale)
            if self.data.close[0] < next_buy_price and self.data.close[0] < self.last_buy_price * (1 - self.params.martingale_percent / 100):
                unit_size_martingale = unit_size * math.pow(self.params.martingale_mult, self.count_martingale)
                self.buy(size=unit_size_martingale)
                self.last_buy_price = self.data.close[0]
                self.count_martingale += 1




def backtest_coin(df,data_signals):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(
        MartingaleStrategy,
        start_position_size=data_signals['start_position_size'],
        take_profit_percent=data_signals['takeprofit'],
        martingale_percent=data_signals['start_martingale_percent'],
        martingale_mult=data_signals["martingale_multiplayer"],
        rsi_length=14,
        rsi_bb_length=20,
        price_bb_length=20,
        deviation=data_signals["bb_deviation"]
    )
    bt_feed = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(bt_feed)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer,_name='tradeanalyzer')
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name='drawdown')
    cash=100000
    cerebro.broker.setcash(cash)
    strats=cerebro.run()
    res_ta =strats[0].analyzers.getbyname('tradeanalyzer').get_analysis()
    res_dd= strats[0].analyzers.getbyname('drawdown').get_analysis()

    res={}
    res['moneydown'] = res_dd.get('max', {}).get('drawdown', 0)
    res['won'] = res_ta.get('won', {}).get('total', 0)
    res['pnl'] = res_ta.get('pnl', {}).get('net', {}).get('total', 0)
    res['pnl_perc'] = res['pnl'] / cash * 100 if cash else 0
    res['pnl_average'] = res_ta.get('pnl', {}).get('net', {}).get('average', 0)
    res['pnl_average_perc'] = res['pnl_average'] / cash * 100 if cash else 0
    res['len_total'] = res_ta.get('len', {}).get('total', 0)
    res['len_average'] = res_ta.get('len', {}).get('average', 0)
    res['len_max'] = res_ta.get('len', {}).get('max', 0)

    return res
