# region imports
from AlgorithmImports import *
from System.Drawing import Color
# endregion

class ForexMeanReversion(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2015, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)

        self.pair = self.add_forex('EURUSD', Resolution.DAILY, Market.Oanda).symbol
        self.bb = self.BB(self.pair, 20, 2)

        stock_plot = Chart('Trade Plot')
        stock_plot.add_series(Series('Buy', SeriesType.SCATTER, "$", Color.Green, ScatterMarkerSymbol.TRIANGLE))
        stock_plot.add_series(Series('Sell', SeriesType.SCATTER, "$", Color.Red, ScatterMarkerSymbol.TRIANGLE_DOWN))
        stock_plot.add_series(Series('Liquidate', SeriesType.SCATTER, "$", Color.Blue, ScatterMarkerSymbol.DIAMOND))
        self.add_chart(stock_plot)

    def on_data(self, data: Slice):
        if not self.bb.is_ready:
            return

        price = data[self.pair].price

        self.plot('Trade Plot', 'Price', price)
        self.plot('Trade Plot', 'Middle Band', self.bb.middle_band.current.value)
        self.plot('Trade Plot', 'Upper Band', self.bb.upper_band.current.value)
        self.plot('Trade Plot', 'Lower Band', self.bb.lower_band.current.value)


        if not self.portfolio.invested:
            if self.bb.lower_band.current.value > price:
                self.set_holdings(self.pair, 1)
                self.plot('Trade Plot', 'Buy', price)
            elif self.bb.upper_band.current.value < price:
                self.set_holdings(self.pair, -1)
                self.plot('Trade Plot', 'Sell', price)

        else:
            if self.portfolio[self.pair].is_long:
                if self.bb.middle_band.current.value < price:
                    self.liquidate()
                    self.plot('Trade Plot', 'Liquidate', price)
            elif self.bb.middle_band.current.value > price:
                self.liquidate()
                self.plot('Trade Plot', 'Liquidate', price)        
