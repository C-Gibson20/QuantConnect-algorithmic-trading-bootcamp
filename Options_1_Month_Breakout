# region imports
from AlgorithmImports import *
# endregion

class OptionsOneMonthBreakoutStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)

        equity = self.add_equity('MSFT', Resolution.MINUTE)
        equity.set_data_normalization_mode(DataNormalizationMode.RAW)
        self.equity = equity.symbol
        self.set_benchmark(self.equity)

        option = self.add_option('MSFT', Resolution.MINUTE)
        option.set_filter(-3, 3, timedelta(20), timedelta(40))

        self.high = self.MAX(self.equity, 21, Resolution.DAILY, Field.high)
        

    def on_data(self, data):
        if not self.high.is_ready:
            return

        option_invested = [x.key for x in self.portfolio if x.value.invested and x.value.type == SecurityType.OPTION]

        if option_invested:
            if self.time + timedelta(4) > option_invested[0].id.date:
                self.liquidate(option_invested[0], 'Too close to expiration')
            return

        if self.securities[self.equity].price >= self.high.current.value:
            for i in data.option_chains:
                chains = i.value
                self.buy_call(chains)
            

    def buy_call(self, chains):
        expiry = sorted(chains, key = lambda x: x.expiry, reverse=True)[0].expiry
        calls = [i for i in chains if i.expiry and i.right == OptionRight.CALL]
        call_contracts = sorted(calls, key = lambda x: abs(x.strike - x.underlying_last_price))

        if len(call_contracts) == 0:
            return
        self.call = call_contracts[0]

        quantity = self.portfolio.total_portfolio_value / self.call.ask_price
        quantity = int( 0.05 * quantity / 100)
        self.buy(self.call.symbol, quantity)
        

    def on_order_event(self, order_event):
        order = self.transactions.get_order_by_id(order_event.order_id)
        if order.type == OrderType.OPTION_EXERCISE:
            self.liquidate()
