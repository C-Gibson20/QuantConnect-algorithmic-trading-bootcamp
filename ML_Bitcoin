# region imports
from AlgorithmImports import *
from tensorflow.keras.models import Sequential, model_from_json
import json
# endregion

class MLBitcoin(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018, 1, 1)
        self.set_end_date(2020, 1, 1)

        model_key = 'bitcoin_price_predictor'
        if self.object_store.contains_key(model_key):
            json_config = self.ObjectStore.Read(model_key)
            self.model = model_from_json(json_config)

        self.set_brokerage_model(BrokerageName.Bitfinex, AccountType.CASH)
        self.set_cash(100000)
        self.symbol = self.add_crypto('BTCUSD', Resolution.DAILY).symbol
        self.set_benchmark(self.symbol)


    def on_data(self, data: Slice):
        if self.get_prediction() == 'Up':
            self.set_holdings(self.symbol, 1)
        else:
            self.set_holdings(self.symbol, -0.5)


    def get_prediction(self):

        df = self.history(self.symbol, 40).loc[self.symbol]
        df_change = df[['open', 'high', 'low', 'close', 'volume']].pct_change().dropna()
        model_input = []

        for index, row in df_change.tail(30).iterrows():
            model_input.append(np.array(row))
            
        model_input = np.array([model_input])

        if round(self.model.predict(model_input)[0][0]) == 0:
            return 'Down'
        else:
            return 'Up'

