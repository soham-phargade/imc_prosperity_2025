from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    def run(self, state):
        result = {}
        fair_price = {
            "RAINFOREST_RESIN": 10000,
            "KELP": 2045.95,
            "SQUID_INK": 1844.78,
        }

        for product, order_depth in state.order_depths.items():
            orders = []
            acceptable_price = fair_price[product]
            current_pos = state.position.get(product, 0)

            # BUY orders
            for ask_price in sorted(order_depth.sell_orders):
                volume = order_depth.sell_orders[ask_price]
                buy_qty = min(-volume, POSITION_LIMIT - current_pos)
                if ask_price < acceptable_price:
                    orders.append(Order(product, ask_price, buy_qty))  # Buy
                    current_pos += buy_qty
                if current_pos >= POSITION_LIMIT:
                    break

            # SELL orders
            for bid_price in sorted(order_depth.buy_orders, reverse=True):
                volume = order_depth.buy_orders[bid_price]
                sell_qty = min(volume, POSITION_LIMIT + current_pos)
                if bid_price > acceptable_price and sell_qty > 0:
                    orders.append(Order(product, bid_price, -sell_qty))
                    current_pos -= sell_qty
                if current_pos <= -POSITION_LIMIT:
                    break

            result[product] = orders

        return result, 0, ""