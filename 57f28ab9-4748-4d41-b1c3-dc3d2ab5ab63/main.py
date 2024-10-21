from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming you have 100 shares of RKLB as your position size.
        # In practice, you'd dynamically fetch this from your brokerage account.
        self.rklb_position_size = 100  
        self.tickers = ["RKLB"]
        self.data_list = [Asset("RKLB")]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Accessing the current price for RKLB.
        current_price_data = data["ohlcv"]
        if current_price_data:
            current_price = current_price_data[-1]["RKLB"]["close"]
            log(f"RKLB current price: {current_price}")

            # Compare current price to your position here.
            # This example simply logs the comparison.
            # Actual trading logic to buy/sell based on this comparison should be implemented as needed.
            log(f"Comparing current price to predefined position size: {self.rklb_position_size} shares.")

            # Example of deciding to maintain current position without changes
            allocation = 0  # This means no change to the current position
        else:
            log("No data available for RKLB.")
            allocation = 0

        # For Surmount, you need to return an allocation between 0 and 1, but since this example doesn't trade:
        # you might display a log or warning instead, or interpret 0 as maintaining a current position without buys/sells.
        return TargetAllocation({"RKLB": allocation})