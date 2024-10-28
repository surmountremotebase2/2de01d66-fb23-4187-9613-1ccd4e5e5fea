from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log


class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "ASTS"
        self.previous_price = None

        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Ensuring the strategy checks the price every minute
        return "5min"

    @property
    def data(self):
        # Not adding OHLCV data to data_list as instructed.
        return []

    def run(self, data):
        # Access the latest minute's close price data for ASTS
        log(f"stofck_data)
        
        stock_data = data["ohlcv"]
        current_price = stock_data[-1][self.ticker]["close"]
        log(f"current: {current_price}; previous: {self.previous_price}")

        if self.previous_price is not None:  
            # Calculate the 5-minute SMA for ASTS. Length is set to 5 for the 5-minute.
            stock_sma_10min = SMA(self.ticker, stock_data, 10)
            stock_sma_5min = SMA(self.ticker, stock_data, 5)
            stock_sma_3min = SMA(self.ticker, stock_data, 3)
            stock_sma_1min = SMA(self.ticker, stock_data, 1)
            
            if len(stock_sma_5min) == 0:
                log(f"not enough data")
                # If we do not have enough data to calculate SMA, we do not return any allocation
                return TargetAllocation({})
            
            # The last value from stock_sma_5min gives us the latest SMA value
            sma_10_min_current = stock_sma_10min[-1]
            sma_5min_current = stock_sma_5min[-1]
            sma_3min_current = stock_sma_3min[-1]
            sma_1min_current = stock_sma_1min[-1]

            sma_1min_1minago = stock_sma_1min[-2]


            price_difference = sma_1min_1minago - sma_1min_current
            log(f"moving avg price difference: {price_difference}; current price: {current_price}")
            
            allocation = 0

            # log(f"difference: ${price_difference}")

            if price_difference < 0:
                log("*** buy ***")
                # TODO: combine current price v previous price with sma
                if -0.01 < price_difference < 0:
                    allocation = 0.55
                
                elif -.02 < price_difference <= -0.01: 
                    allocation = 0.6

                elif -.05 < price_difference <= -0.03: 
                    allocation = 0.75

                elif -.10 < price_difference <= -0.05: 
                    allocation = 0.80

                elif -.10 > price_difference: 
                    allocation = 1

            elif price_difference > 1:
                log("$$$ sell $$$")
                if current_price > sma_3min_current:
                    allocation = 0.25
                elif current_price > sma_5min_current: 
                    allocation = 0

        else:
            log(f'{self.ticker} no conditions met; holding position')
            
        # Update the previous price with the current price for the next run.
        self.previous_price = current_price

        # Returning the target allocation based on the logic above
        return TargetAllocation({self.ticker: allocation})