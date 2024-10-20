
from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming "PL" is the ticker symbol for Planet Labs. Replace with the correct symbol if necessary.
        self.ticker = "PL"
        self.previous_price = None

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Setting the data interval to 1 minute.
        return "1min"

    def run(self, data):
        # Fetch the last closing price of Planet Labs from the OHLCV data.
        current_price = data["ohlcv"][-1][self.ticker]["close"]
        
        # Initialize target allocation with no change initially.
        target_allocation = 0.5  # Assuming a neutral position where 0.5 does not indicate buying or selling. Adjust accordingly.
        
        # Check if the previous price is set. If not, this is the first run.
        if self.previous_price is not None:
            price_change = current_price - self.previous_price
            
            # If price is up by at least $0.05, sell (set allocation to 0).
            if price_change >= 0.05:
                target_allocation = 0
                log(f"Price increased by ${price_change} to ${current_price}. Setting target allocation for {self.ticker} to {target_allocation} (SELL).")
            
            # If price is down by at least $0.05, buy (set allocation to 1).
            elif price_change <= -0.02:
                target_allocation = 1
                log(f"Price decreased by ${price_change} to ${current_price}. Setting target allocation for {self.ticker} to {target_allocation} (BUY).")
        
        # Update the previous price with the current price for the next run.
        self.previous_price = current_price
        
        # Return the target allocation for the strategy.
        return TargetAllocation({self.ticker: target_allocation})
