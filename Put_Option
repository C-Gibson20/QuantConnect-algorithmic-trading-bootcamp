# region imports
from AlgorithmImports import *
# endregion

class PutOption(QCAlgorithm):

    def Initialize(self):
        self.set_start_date(2017, 10, 1)
        self.set_end_date(2020, 10, 1)
        self.set_cash(100000)

        self.equity = self.add_equity("SPY", Resolution.MINUTE)
        self.equity.set_data_normalization_mode(DataNormalizationMode.RAW)
        self.symbol = self.equity.symbol

        self.vix = self.add_data(CBOE, "VIX").symbol

        self.rank = 0
        
        self.contract = str()
        self.contracts_added = set()
        
        self.days_before_exp = 2 # Number of days before expiry to exit
        self.DTE = 25 # Target days till expiration
        self.OTM = 0.01 # Target percentage OTM of put
        self.lookback_IV = 150 # Lookback length of IV indicator
        self.IV_lvl = 0.5 # Enter position at this lvl of IV indicator
        self.percentage = 0.9 # Percentage of portfolio for underlying asset
        self.options_alloc = 90 # 1 option for X num of shares (balanced would be 100)
        
        self.schedule.on(self.date_rules.every_day(self.symbol), self.time_rules.after_market_open(self.symbol, 30), self.plotting)
        self.schedule.on(self.date_rules.every_day(self.symbol), self.time_rules.after_market_open(self.symbol, 30), self.VIX_rank)
        
        self.set_warm_up(timedelta(self.lookback_IV)) 

    def VIX_rank(self):
        history = self.history(CBOE, self.vix, self.lookback_IV, Resolution.DAILY)
        # (Current - Min) / (Max - Min)
        self.rank = ((self.securities[self.vix].price - min(history["low"])) / (max(history["high"]) - min(history["low"])))
 
    def on_data(self, data):
        if(self.is_warming_up):
            return
        
        # Buy underlying asset
        if not self.portfolio[self.symbol].invested:
            self.set_holdings(self.symbol, self.percentage)
        
        # Buy put if VIX relatively high
        if self.rank > self.IV_lvl:
            self.buy_put(data)
        
        # Close put before it expires
        if self.contract:
            if (self.contract.id.date - self.time) <= timedelta(self.days_before_exp):
                self.liquidate(self.contract)
                self.log("Closed: too close to expiration")
                self.contract = str()

    def buy_put(self, data):
        if self.contract == str():
            self.contract = self.options_filter(data)
            return
        
        elif not self.portfolio[self.contract].invested and data.contains_key(self.contract):
            self.buy(self.contract, round(self.portfolio[self.symbol].quantity / self.options_alloc))

    def options_filter(self, data):
        contracts = self.option_chain_provider.get_option_contract_list(self.symbol, data.time)
        self.underlying_price = self.securities[self.symbol].price

        # Filter the out-of-money put options from the contract list which expire close to self.DTE num of days from now
        otm_puts = [i for i in contracts if i.ID.OptionRight == OptionRight.PUT and
                                            self.underlying_price - i.ID.StrikePrice > self.OTM * self.underlying_price and
                                            self.DTE - 8 < (i.ID.date - data.time).days < self.DTE + 8]
        if len(otm_puts) > 0:
            # Sort options by closest to self.DTE days from now and desired strike, and pick first
            contract = sorted(sorted(otm_puts, key = lambda x: abs((x.ID.date - self.time).days - self.DTE)),
                                                     key = lambda x: self.underlying_price - x.ID.StrikePrice)[0]
            if contract not in self.contracts_added:
                self.contracts_added.add(contract)
                
                # Use AddOptionContract() to subscribe the data for specified contract
                self.add_option_contract(contract, Resolution.MINUTE)

            return contract
        else:
            return str()

    def plotting(self):
        self.plot("Vol Chart", "Rank", self.rank)
        self.plot("Vol Chart", "lvl", self.IV_lvl)
        self.plot("Data Chart", self.symbol, self.securities[self.symbol].close)
        
        option_invested = [x.key for x in self.portfolio if x.Value.invested and x.Value.Type==SecurityType.OPTION]
        if option_invested:
                self.Plot("Data Chart", "strike", option_invested[0].ID.StrikePrice)

    def on_order_event(self, orderEvent):
        self.log(str(orderEvent))
