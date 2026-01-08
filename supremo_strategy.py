"""
Supremo All-In-One Strategy Module
Implements trend filters, entry zones, TP/SL logic, and risk management.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class SupremoStrategy:
    """
    Supremo All-In-One Trading Strategy
    
    Logic:
    - Trend Filter: Bullish if Price > EMA 50 > EMA 200; Bearish if Price < EMA 50 < EMA 200
    - Entry Zones: Long at ML/WO (Bullish), Short at MH/PWH (Bearish)
    - TP: Next logical range level
    - SL: 1 ATR or fixed % below entry
    """
    
    def __init__(self):
        """Initialize strategy with configuration."""
        self.risk_per_trade = float(os.getenv('RISK_PER_TRADE', '1.0'))  # 1% default
        self.total_equity = float(os.getenv('TOTAL_EQUITY', '10000'))  # Default equity
        self.atr_period = int(os.getenv('ATR_PERIOD', '14'))
        self.atr_multiplier = float(os.getenv('ATR_MULTIPLIER', '1.0'))
        self.fixed_sl_percent = float(os.getenv('FIXED_SL_PERCENT', '0'))  # 0 = use ATR
        
        # Signal deduplication
        self.last_signal_time = {}
        self.deduplication_window = 15 * 60  # 15 minutes in seconds
    
    def check_trend_filter(self, price: float, ema50: float, ema200: float) -> str:
        """
        Determine trend bias based on EMA relationship.
        
        Args:
            price: Current price
            ema50: EMA 50 value
            ema200: EMA 200 value
            
        Returns:
            'bullish' or 'bearish'
        """
        if price > ema50 > ema200:
            return 'bullish'
        elif price < ema50 < ema200:
            return 'bearish'
        else:
            # Neutral/choppy - return based on price vs EMA50
            return 'bullish' if price > ema50 else 'bearish'
    
    def validate_entry_zone(
        self, 
        action: str, 
        trend_bias: str, 
        entry_level: str,
        price: float,
        ml: float = None,
        mh: float = None,
        wo: float = None,
        pwh: float = None
    ) -> bool:
        """
        Validate if entry conditions are met.
        
        Args:
            action: 'buy' or 'sell'
            trend_bias: 'bullish' or 'bearish'
            entry_level: 'ML', 'WO', 'MH', 'PWH'
            price: Current price
            ml: Monday Low
            mh: Monday High
            wo: Weekly Open
            pwh: Previous Week High
            
        Returns:
            True if entry is valid, False otherwise
        """
        if action == 'buy':
            # Long entries require bullish trend
            if trend_bias != 'bullish':
                return False
            
            # Check if price is at entry level
            if entry_level == 'ML' and ml:
                # Price should be touching/sweeping ML (within 0.1% tolerance)
                return abs(price - ml) / ml <= 0.001
            elif entry_level == 'WO' and wo:
                return abs(price - wo) / wo <= 0.001
            else:
                return False
                
        elif action == 'sell':
            # Short entries require bearish trend
            if trend_bias != 'bearish':
                return False
            
            # Check if price is at entry level
            if entry_level == 'MH' and mh:
                return abs(price - mh) / mh <= 0.001
            elif entry_level == 'PWH' and pwh:
                return abs(price - pwh) / pwh <= 0.001
            else:
                return False
        
        return False
    
    def calculate_take_profit(
        self,
        entry_level: str,
        entry_price: float,
        ml: float = None,
        mm: float = None,
        mh: float = None,
        wo: float = None,
        pwh: float = None
    ) -> Tuple[float, float]:
        """
        Calculate TP1 and TP2 based on entry level.
        
        Args:
            entry_level: Entry level identifier ('ML', 'WO', 'MH', 'PWH')
            entry_price: Entry price
            ml: Monday Low
            mm: Monday Mid
            mh: Monday High
            wo: Weekly Open
            pwh: Previous Week High
            
        Returns:
            Tuple of (TP1, TP2)
        """
        tp1 = None
        tp2 = None
        
        if entry_level == 'ML':
            # Long from ML: TP1 = Monday Mid, TP2 = Monday High
            if mm:
                tp1 = mm
            if mh:
                tp2 = mh
        elif entry_level == 'WO':
            # Long from WO: TP1 = Monday Mid, TP2 = Monday High
            if mm:
                tp1 = mm
            if mh:
                tp2 = mh
        elif entry_level == 'MH':
            # Short from MH: TP1 = Monday Mid, TP2 = Monday Low
            if mm:
                tp1 = mm
            if ml:
                tp2 = ml
        elif entry_level == 'PWH':
            # Short from PWH: TP1 = Monday High, TP2 = Monday Mid
            if mh:
                tp1 = mh
            if mm:
                tp2 = mm
        
        # Fallback: Use percentage-based TPs if levels not provided
        if tp1 is None:
            tp1 = entry_price * 1.01  # 1% above entry for longs
        if tp2 is None:
            tp2 = entry_price * 1.02  # 2% above entry for longs
        
        return (tp1, tp2)
    
    def calculate_stop_loss(
        self,
        entry_price: float,
        atr: float = None,
        action: str = 'buy'
    ) -> float:
        """
        Calculate stop loss: 1 ATR or fixed %.
        
        Args:
            entry_price: Entry price
            atr: ATR value (optional)
            action: 'buy' or 'sell'
            
        Returns:
            Stop loss price
        """
        if self.fixed_sl_percent > 0:
            # Use fixed percentage
            if action == 'buy':
                return entry_price * (1 - self.fixed_sl_percent / 100)
            else:
                return entry_price * (1 + self.fixed_sl_percent / 100)
        elif atr:
            # Use ATR
            if action == 'buy':
                return entry_price - (atr * self.atr_multiplier)
            else:
                return entry_price + (atr * self.atr_multiplier)
        else:
            # Default: 1% stop loss
            if action == 'buy':
                return entry_price * 0.99
            else:
                return entry_price * 1.01
    
    def calculate_position_size(
        self,
        entry_price: float,
        stop_loss: float,
        action: str = 'buy'
    ) -> float:
        """
        Calculate position size based on 1% risk of total equity.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            action: 'buy' or 'sell'
            
        Returns:
            Position size (quantity)
        """
        # Calculate risk per share
        if action == 'buy':
            risk_per_share = entry_price - stop_loss
        else:
            risk_per_share = stop_loss - entry_price
        
        if risk_per_share <= 0:
            return 0
        
        # Total risk amount (1% of equity)
        total_risk = self.total_equity * (self.risk_per_trade / 100)
        
        # Position size
        position_size = total_risk / risk_per_share
        
        return round(position_size, 8)  # Round to 8 decimals for crypto
    
    def check_deduplication(self, ticker: str, timestamp: str) -> bool:
        """
        Check if signal should be ignored due to deduplication.
        
        Args:
            ticker: Trading symbol
            timestamp: Signal timestamp
            
        Returns:
            True if signal should be ignored, False if it's new
        """
        try:
            # Parse timestamp (assuming ISO format or Unix timestamp)
            if isinstance(timestamp, str):
                if timestamp.isdigit():
                    signal_time = int(timestamp)
                else:
                    # Try parsing ISO format
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    signal_time = int(dt.timestamp())
            else:
                signal_time = int(timestamp)
            
            # Check if we've seen a signal for this ticker recently
            if ticker in self.last_signal_time:
                time_diff = signal_time - self.last_signal_time[ticker]
                if time_diff < self.deduplication_window:
                    return True  # Ignore duplicate
            
            # Update last signal time
            self.last_signal_time[ticker] = signal_time
            return False  # New signal
            
        except Exception as e:
            print(f"Error in deduplication check: {e}")
            return False  # Allow signal if parsing fails
    
    def process_signal(self, payload: Dict) -> Optional[Dict]:
        """
        Process a TradingView webhook signal.
        
        Args:
            payload: Webhook payload from TradingView
            
        Returns:
            Processed signal dict with all calculated values, or None if invalid
        """
        try:
            ticker = payload.get('ticker')
            action = payload.get('action', '').lower()
            price = float(payload.get('price', 0))
            sl = payload.get('sl')
            tp = payload.get('tp')
            trend_bias = payload.get('trend_bias', '').lower()
            timestamp = payload.get('timestamp', datetime.now().isoformat())
            
            # Validate required fields
            if not all([ticker, action, price]):
                print("❌ Missing required fields in signal")
                return None
            
            if action not in ['buy', 'sell']:
                print(f"❌ Invalid action: {action}")
                return None
            
            # Check deduplication
            if self.check_deduplication(ticker, timestamp):
                print(f"⚠️  Duplicate signal ignored for {ticker}")
                return None
            
            # Extract entry level from payload (if provided)
            entry_level = payload.get('entry_level', '')
            
            # Calculate stop loss if not provided
            if sl:
                try:
                    stop_loss = float(sl)
                except:
                    stop_loss = self.calculate_stop_loss(price, action=action)
            else:
                atr = payload.get('atr')
                atr = float(atr) if atr else None
                stop_loss = self.calculate_stop_loss(price, atr=atr, action=action)
            
            # Calculate take profit if not provided
            if tp:
                try:
                    tp1 = float(tp)
                    tp2 = tp1 * 1.01  # Default TP2
                except:
                    tp1, tp2 = self.calculate_take_profit(entry_level, price)
            else:
                tp1, tp2 = self.calculate_take_profit(entry_level, price)
            
            # Calculate position size
            position_size = self.calculate_position_size(price, stop_loss, action)
            
            # Build signal dict
            signal = {
                'ticker': ticker,
                'action': action,
                'entry_price': price,
                'stop_loss': stop_loss,
                'tp1': tp1,
                'tp2': tp2,
                'trend_bias': trend_bias,
                'entry_level': entry_level,
                'position_size': position_size,
                'risk_amount': self.total_equity * (self.risk_per_trade / 100),
                'timestamp': timestamp,
                'processed_at': datetime.now().isoformat()
            }
            
            return signal
            
        except Exception as e:
            print(f"❌ Error processing signal: {e}")
            return None
    
    def format_signal_message(self, signal: Dict) -> str:
        """
        Format signal as a readable message for notifications.
        
        Args:
            signal: Processed signal dictionary
            
        Returns:
            Formatted message string
        """
        action_emoji = "🟢" if signal['action'] == 'buy' else "🔴"
        trend_emoji = "📈" if signal['trend_bias'] == 'bullish' else "📉"
        
        message = f"""
{action_emoji} SUPREMO SIGNAL - {signal['ticker']}

Action: {signal['action'].upper()}
Entry Price: ${signal['entry_price']:,.2f}
Entry Level: {signal.get('entry_level', 'N/A')}
Trend: {trend_emoji} {signal['trend_bias'].upper()}

Stop Loss: ${signal['stop_loss']:,.2f}
Take Profit 1: ${signal['tp1']:,.2f}
Take Profit 2: ${signal['tp2']:,.2f}

Position Size: {signal['position_size']:.8f}
Risk Amount: ${signal['risk_amount']:,.2f} ({self.risk_per_trade}% of equity)

Time: {signal['timestamp']}
"""
        return message.strip()

