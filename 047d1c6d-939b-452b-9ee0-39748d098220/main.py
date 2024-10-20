from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker you are interested in
        self.ticker = "LUNR"
        # Starting capital (this variable is for illustration, cannot be directly used for trading decisions in Surmount Strategy)
        self.starting_capital = 200
        self.buy_threshold = -0.05  # Buy when the price drops by this amount ($)
        self.sell_threshold = 0.07  # Sell when the price increases by this amount ($)
        # Instantiated data list should be empty according to Surmount's conventions
        self.data_list = []

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1min"

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}

        # Access the latest two close prices
        if len(data["ohlcv"]) > 1:
            current_close = data["ohlcv"][-1][self.ticker]["close"]
            previous_close = data["ohlcv"][-2][self.ticker]["close"]
            price_change = current_close - previous_close

            # Determine action based on price change
            if price_change <= self.buy_threshold:
                # Scenario to buy LUNR, setting allocation to a hypothetical maximum affordance
                # (actual buying power calculation needs account info)
                log("Buying LUNR")
                allocation_dict[self.ticker] = 1  # This is a simplified representation; adjust based on actual capital and price
            elif price_change >= self.sell_threshold:
                # Scenario to sell LUNR, removing allocation
                log("Selling LUNR")
                allocation_dict[self.ticker] = 0  # Remove allocation
            else:
                # No action taken
                log("No action taken")
        else:
            log("Not enough data to make a decision")

        return TargetAllocation(allocation_dict)