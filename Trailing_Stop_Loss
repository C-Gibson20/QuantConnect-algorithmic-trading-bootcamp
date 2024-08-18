# region imports
from AlgorithmImports import *
# endregion

class TrailingStopLossStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2018, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)
        
        self.qqq = self.add_equity("QQQ", Resolution.HOUR).symbol

        self.entry_ticket = None
        self.stop_market_ticket = None
        self.entry_time = datetime.min
        self.stop_market_order_fill_time = datetime.min
        self.highest_price = 0
        

    def on_data(self, data: Slice):

        # Wait 30 days after last exit
        if (self.time - self.stop_market_order_fill_time).days < 30:
            return
            
        price = self.securities[self.qqq].price

        # Send entry limit order
        if not self.portfolio.invested and not self.transactions.get_open_orders(self.qqq):
            quantity = self.calculate_order_quantity(self.qqq, 0.9)
            self.entry_ticket = self.limit_order(self.qqq, quantity, price, "Entry Order")
            self.entry_time = self.time

        # Move limit price if order not filled after 1 day
        if (self.time - self.entry_time).days > 1 and self.entry_ticket.status != OrderStatus.FILLED:
            self.entry_time = self.time
            update_fields = UpdateOrderFields()
            update_fields.limit_price = price
            self.entry_ticket.update(update_fields)


        # Move up trailing stop price
        if self.stop_market_ticket is not None and self.portfolio.invested:
            if price > self.highest_price:
                self.highest_price = price
                update_fields = UpdateOrderFields()
                update_fields.stop_price = price * 0.95
                self.stop_market_ticket.update(update_fields)
                # self.Debug(update_fields.stop_price)


    def on_order_event(self, order_event):
        if order_event.status != OrderStatus.FILLED:
            return
        
        # Send stop loss order if entry limit order is filled
        if self.entry_ticket is not None and self.entry_ticket.order_id == order_event.order_id:
            self.stop_market_ticket = self.stop_market_order(self.qqq, -self.entry_ticket.quantity, 0.95 * self.entry_ticket.average_fill_price)

        # Save fill time of stop loss order
        if self.stop_market_ticket is not None and self.stop_market_ticket.order_id == order_event.order_id:
            self.stop_market_order_fill_time = self.time
            self.highest_price = 0
