# region imports
from AlgorithmImports import *
# endregion

class SizeFactorStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)

        self.rebalance_time = datetime.min
        self.active_stocks = set()

        self.add_universe(self.coarse_filter, self.fine_filter)
        self.universe_settings.resolution = Resolution.HOUR

        self.portfolio_targets = []

    
    def coarse_filter(self, coarse):
        if self.time <= self.rebalance_time:
            return self.universe.unchanged
        
        self.rebalance_time = self.time + timedelta(30)

        sorted_by_dollar_volume = sorted(coarse, key = lambda x: x.dollar_volume, reverse = True)

        return [x.symbol for x in sorted_by_dollar_volume if x.price > 10 and x.has_fundamental_data ][:200]
    
    def fine_filter(self, fine):
        sorted_by_pe = sorted(fine, key = lambda x: x.market_cap)
        return [x.symbol for x in sorted_by_pe if x.market_cap > 0][:10]
        

    def on_securities_changed(self, changes):
        for x in changes.removed_securities:
            self.liquidate(x.symbol)
            self.active_stocks.remove(x.symbol)

        for x in changes.added_securities:
            self.active_stocks.add(x.symbol)

        self.portfolio_targets = [PortfolioTarget(symbol, 1/len(self.active_stocks)) for symbol in self.active_stocks]

    def on_data(self, data: Slice):
        
        if self.portfolio_targets == []:
            return

        for symbol in self.active_stocks:
            if symbol not in data:
                return

        self.set_holdings((self.portfolio_targets))
        self.portfolio_targets = []
