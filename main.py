"""
Trading Notification Bot
Monitors cryptocurrency prices and sends notifications when conditions are met.
"""

import os
import sys
import time
from dotenv import load_dotenv
from exchange_api import get_current_price
from notification import send_notification

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        # Fallback for older Python versions
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Load environment variables
load_dotenv()


class TradingBot:
    """Main trading bot class that monitors prices and sends alerts."""
    
    def __init__(self):
        """Initialize bot with configuration from environment variables."""
        self.symbol = os.getenv('SYMBOL', 'BTCUSDT')
        self.threshold_above = float(os.getenv('PRICE_THRESHOLD_ABOVE', '50000'))
        self.threshold_below = float(os.getenv('PRICE_THRESHOLD_BELOW', '45000'))
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '60'))
        self.last_price = None
        self.last_alert_price = None
        
    def check_conditions(self, current_price):
        """
        Check if price conditions are met.
        
        Args:
            current_price: Current price of the symbol
            
        Returns:
            List of alert messages
        """
        alerts = []
        
        # Check if price crossed above threshold
        if current_price >= self.threshold_above:
            if self.last_price is None or self.last_price < self.threshold_above:
                alerts.append(
                    f"🚀 ALERT: {self.symbol} price is above ${self.threshold_above:,.2f}\n"
                    f"Current price: ${current_price:,.2f}"
                )
        
        # Check if price crossed below threshold
        if current_price <= self.threshold_below:
            if self.last_price is None or self.last_price > self.threshold_below:
                alerts.append(
                    f"📉 ALERT: {self.symbol} price is below ${self.threshold_below:,.2f}\n"
                    f"Current price: ${current_price:,.2f}"
                )
        
        return alerts
    
    def run(self):
        """Main bot loop that continuously monitors prices."""
        print(f"🤖 Trading Bot Started")
        print(f"📊 Monitoring: {self.symbol}")
        print(f"🔔 Alert thresholds: Above ${self.threshold_above:,.2f} | Below ${self.threshold_below:,.2f}")
        print(f"⏱️  Check interval: {self.check_interval} seconds")
        print("-" * 50)
        
        while True:
            try:
                # Get current price
                current_price = get_current_price(self.symbol)
                
                if current_price:
                    # Check for alerts
                    alerts = self.check_conditions(current_price)
                    
                    # Send notifications if alerts exist
                    if alerts:
                        for alert in alerts:
                            send_notification(alert)
                            print(f"✅ Alert sent: {alert}")
                    
                    # Display current status
                    price_change = ""
                    if self.last_price:
                        change = current_price - self.last_price
                        change_pct = (change / self.last_price) * 100
                        price_change = f" ({change:+.2f}, {change_pct:+.2f}%)"
                    
                    print(f"💰 {self.symbol}: ${current_price:,.2f}{price_change}")
                    
                    self.last_price = current_price
                else:
                    print("⚠️  Failed to fetch price. Retrying...")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("⏳ Retrying in 60 seconds...")
                time.sleep(60)


if __name__ == "__main__":
    bot = TradingBot()
    bot.run()

