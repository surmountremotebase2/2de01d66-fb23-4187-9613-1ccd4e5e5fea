from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        # Indicates that this strategy is applicable to RKLB
        return ["RKLB"]
    
    @property
    def interval(self):
        # The interval for the strategy - 1hour intervals could capture mean reversion well.
        # Adjust based on the desired frequency and nature of trading.
        return "1hour"
    
    def run(self, data):
        # Initialize the allocation for RKLB to 0 indicating no position.
        rklb_stake = 0
        # MACD calculation for RKLB
        macd_data = MACD("RKLB", data["ohlcv"], fast=12, slow=26)
        if macd_data is not None:
            macd_line = macd_data["MACD"]
            signal_line = macd_data["signal"]
            
            if len(macd_line) > 1 and len(signal_line) > 1:
                current_macd = macd_line[-1]
                previous_macd = macd_line[-2]
                current_signal = signal_line[-1]
                previous_signal = signal_line[-2]
                
                # Buy signal: MACD crosses above the signal line
                if current_macd > current_signal and previous_macd <= previous_signal:
                    log(f"Buy signal for RKLB. MACD: {current_macd}, Signal: {current_signal}")
                    rklb_stake = 1  # Allocate 100% to RKLB (this strategy manages only one asset)
                    
                # Sell/Exit signal: MACD crosses below the signal line
                elif current_macd < current_signal and previous_macd >= previous_signal:
                    log(f"Sell signal for RKLB. MACD: {current_macd}, Signal: {current_signal}")
                    rklb_stake = 0  # Exit the position by allocating 0
                
        # Return the target allocation for RKLB based on the signals.
        return TargetAllocation({"RKLB": rklb_stake})