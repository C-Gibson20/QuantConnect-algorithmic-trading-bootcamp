# region imports
from AlgorithmImports import *
# endregion

class DayTrading(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)
        self.symbol = self.add_equity("SPY", Resolution.MINUTE).symbol
        self.rolling_window = RollingWindow[TradeBar](2)
        self.consolidate(self.symbol, Resolution.DAILY, self.custom_bar_handler)

        self.schedule.on(self.date_rules.every_day(self.symbol),
                         self.time_rules.before_market_close(self.symbol, 15),
                         self.exit_positions)


    def on_data(self, data: Slice):
        if not self.rolling_window.is_ready:
            return

        if not (self.time.hour == 9 and self.time.minute == 31):
            return
        
        if data[self.symbol].open >= 1.01 * self.rolling_window[0].close:
            self.set_holdings(self.symbol, -1)
        
        elif data[self.symbol].open <= 0.99 * self.rolling_window[0].close:
            self.set_holdings(self.symbol, 1)


    def custom_bar_handler(self, bar):
        self.rolling_window.add(bar)


    def exit_positions(self):
        self.liquidate((self.symbol))
