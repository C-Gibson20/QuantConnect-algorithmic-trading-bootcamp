# region imports
from AlgorithmImports import *
from collections import deque
# endregion

class SMAStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)
        self.spy = self.add_equity('SPY', Resolution.DAILY).symbol
        
        # # Initialize SMA indicator with a 30-day period
        # self.sma = self.SMA(self.spy, 30, Resolution.DAILY)
        
        # # Warm up the SMA indicator using historical data
        # self.warm_up_indicator(self.spy, self.sma, Resolution.DAILY)

        self.sma = CustomSimpleMovingAverage('CustomSMA', 30)
        self.register_indicator(self.spy, self.sma, Resolution.DAILY)
        
        # Initialize MIN and MAX indicators for 1 year (365 days)
        self.low = self.min(self.spy, 252, Resolution.DAILY)
        self.high = self.max(self.spy, 252, Resolution.DAILY)
        
        # Warm up the MIN and MAX indicators using historical data
        self.warm_up_indicator(self.spy, self.low, Resolution.DAILY)
        self.warm_up_indicator(self.spy, self.high, Resolution.DAILY)


    def on_data(self, data: Slice):

        if not self.sma.is_ready or not self.low.is_ready or not self.high.is_ready:
            return
        
        price = self.securities[self.spy].close

        if price * 1.05 >= self.high.current.value and self.sma.current.value < price:
            if not self.portfolio[self.spy].is_long:
                self.set_holdings(self.spy, 1)
        
        elif price * 0.95 <= self.low.current.value and self.sma.current.value > price:
            if not self.portfolio[self.spy].is_short:
                self.set_holdings(self.spy, -1)
        
        else:
            self.liquidate()
        
        self.plot('Benchmark', '52w-High', self.high.current.value)
        self.plot('Benchmark', '52w-Low', self.low.current.value)
        self.plot('Benchmark', 'SMA', self.sma.current.value)

class CustomSimpleMovingAverage(PythonIndicator):

    def __init__(self, name, period):
        self.name = name
        self.time = datetime.min
        self.value = 0
        self.queue = deque(maxlen=period)
    
    def update(self, input):
        self.queue.appendleft(input.close)
        self.time = input.end_time
        count = len(self.queue)
        self.value = sum(self.queue) / count
        return (count == self.queue.maxlen)
