# region imports
from AlgorithmImports import *
# endregion

class FundamentalFactorAlphaModel(AlphaModel):

    def __init__(self):
        self.rebalance_time = datetime.min
        self.sectors = {}


    def update(self, algorithm, data):
        if algorithm.time <= self.rebalance_time:
            return []
        self.rebalance_time = Expiry.EndOfQuarter(algorithm.time)

        insights = []

        for sector in self.sectors:
            securities = self.sectors[sector]
            sorted_by_ROE = sorted(securities, key = lambda x: x.fundamentals.OperationRatios.ROE.value, reverse = True)
            sorted_by_PM = sorted(securities, key = lambda x: x.fundamentals.OperationRatios.NetMargin.value, reverse = True)
            sorted_by_PE = sorted(securities, key = lambda x: x.fundamentals.ValuationRatios.PERatio, reverse = False)

            scores = {}
            for security in securities:
                score = sum([sorted_by_ROE.index(security), sorted_by_PM.index(security), sorted_by_PE.index(security)])
                scores[security] = score

            length = max(int(len(scores)/5), 1)
            for security in sorted(scores.items(), key = lambda x: x[1], reverse=False)[:length]:
                symbol = security[0].symbol
                insights.append(Insight.price(symbol, Expiry.EndOfQuarter, InsightDirection.UP))

        return insights


    def on_securities_changed(self, algorithm, changes):
        for security in changes.removed_securities:
            for sector in self.sectors:
                if security in self.sectors[sector]:
                    self.sectors[sector].remove(security)

        for security in changes.added_securities:
            sector = security.fundamentals.AssetClassification.MorningstarSectorCode
            if sector not in self.sectors:
                self.sectors[sector] = set()
            self.sectors[sector].add(security)
