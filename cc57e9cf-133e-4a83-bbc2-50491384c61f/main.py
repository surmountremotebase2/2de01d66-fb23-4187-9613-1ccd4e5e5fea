from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log


class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "CLOV"
        self.previous_price = None

        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Ensuring the strategy checks the price every minute
        return "1min"

    @property
    def data(self):
        # Not adding OHLCV data to data_list as instructed.
        return []

    def run(self, data):
        # Access the latest minute's close price data for CLOV
        clov_data = data["ohlcv"]
        current_price = clov_data[-1][self.ticker]["close"]

        if self.previous_price is not None:
           price_difference = current_price - self.previous_price
        
        # Calculate the 5-minute SMA for CLOV. Length is set to 5 for the 5-minute SMA.
        clov_sma_10min = SMA(self.ticker, clov_data, 10)
        clov_sma_5min = SMA(self.ticker, clov_data, 5)
        clov_sma_3min = SMA(self.ticker, clov_data, 3)
        clov_sma_1min = SMA(self.ticker, clov_data, 1)
        
        if len(clov_sma_5min) == 0:
            # If we do not have enough data to calculate SMA, we do not return any allocation
            return TargetAllocation({})
        
        # The last value from clov_sma_5min gives us the latest SMA value
        sma_10_min_current = clov_sma_10min[-1]
        sma_5min_current = clov_sma_5min[-1]
        sma_3min_current = clov_sma_3min[-1]
        sma_1min_current = clov_sma_1min[-1]
        
        allocation = 0

        # log(f"difference: ${price_difference}")

        
        # TODO: combine current price v previous price with sma
        if -0.01 < price_difference < 0:
            allocation = 0.55
        
        elif -.02 < price_difference <= -0.01: 
            allocation = 0.6

        elif -.03 < price_difference <= -0.05: 
            allocation = 0.75

        elif -.05 < price_difference <= -0.10: 
            allocation = 0.80

        elif -.10 < price_difference: 
            allocation = 1

        elif price_difference > 0 and current_price > sma_3min_current:
            allocation = 0

        else:
            log(f'{self.ticker} no conditions met; holding position')
            
        # Update the previous price with the current price for the next run.
        self.previous_price = current_price

        # Returning the target allocation based on the logic above
        return TargetAllocation({self.ticker: allocation})