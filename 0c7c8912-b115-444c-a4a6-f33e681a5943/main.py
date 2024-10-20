
from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "RKLB"  # Assuming RocketLab's ticker is RKLB
        self.prev_close_price = None  # To store the previous close price

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Adjust based on available data intervals

    def run(self, data):
        # Retrieve the latest OHLCV data for RocketLab
        latest_data = data["ohlcv"][-1][self.ticker]
        current_close = latest_data["close"]
        
        allocation = 0  # Default allocation is 0, indicating not to hold the asset
        
        if self.prev_close_price is not None:
            price_change = current_close - self.prev_close_price

            # If the stock went down by 5 cents or more, set allocation to buy (invest fully)
            if price_change <= -0.05:
                allocation = 1  
            # If the stock went up by 10 cents or more, set allocation to sell (divest completely)
            elif price_change >= 0.10:
                allocation = 0  

        # Update the previous close price with the current close price for the next interval comparison
        self.prev_close_price = current_close

        return TargetAllocation({self.ticker: allocation})
