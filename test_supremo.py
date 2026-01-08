"""
Test script for Supremo strategy integration.
Tests signal processing and risk management calculations.
"""

import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from supremo_strategy import SupremoStrategy


def test_signal_processing():
    """Test signal processing with sample payloads."""
    print("🧪 Testing Supremo Strategy Signal Processing")
    print("=" * 50)
    
    strategy = SupremoStrategy()
    
    # Test 1: Long signal at Monday Low
    print("\n📊 Test 1: Long Entry at Monday Low")
    print("-" * 50)
    
    payload1 = {
        "ticker": "BTCUSDT",
        "action": "buy",
        "price": "45000.00",
        "sl": "44500.00",
        "tp": "45500.00",
        "trend_bias": "bullish",
        "timestamp": datetime.now().isoformat(),
        "entry_level": "ML",
        "atr": "500.00"
    }
    
    signal1 = strategy.process_signal(payload1)
    if signal1:
        print("✅ Signal processed successfully")
        print(f"   Entry: ${signal1['entry_price']:,.2f}")
        print(f"   Stop Loss: ${signal1['stop_loss']:,.2f}")
        print(f"   TP1: ${signal1['tp1']:,.2f}")
        print(f"   TP2: ${signal1['tp2']:,.2f}")
        print(f"   Position Size: {signal1['position_size']:.8f}")
        print(f"   Risk Amount: ${signal1['risk_amount']:,.2f}")
        print("\n📨 Formatted Message:")
        print(strategy.format_signal_message(signal1))
    else:
        print("❌ Signal processing failed")
    
    # Test 2: Short signal at Monday High
    print("\n📊 Test 2: Short Entry at Monday High")
    print("-" * 50)
    
    payload2 = {
        "ticker": "ETHUSDT",
        "action": "sell",
        "price": "3000.00",
        "sl": "3050.00",
        "tp": "2950.00",
        "trend_bias": "bearish",
        "timestamp": datetime.now().isoformat(),
        "entry_level": "MH",
        "atr": "50.00"
    }
    
    signal2 = strategy.process_signal(payload2)
    if signal2:
        print("✅ Signal processed successfully")
        print(f"   Entry: ${signal2['entry_price']:,.2f}")
        print(f"   Stop Loss: ${signal2['stop_loss']:,.2f}")
        print(f"   Position Size: {signal2['position_size']:.8f}")
        print(f"   Risk Amount: ${signal2['risk_amount']:,.2f}")
    else:
        print("❌ Signal processing failed")
    
    # Test 3: Deduplication
    print("\n📊 Test 3: Signal Deduplication")
    print("-" * 50)
    
    payload3 = payload1.copy()
    signal3 = strategy.process_signal(payload3)
    if signal3:
        print("❌ Deduplication failed - duplicate signal was processed")
    else:
        print("✅ Deduplication working - duplicate signal ignored")
    
    # Test 4: Trend filter
    print("\n📊 Test 4: Trend Filter Logic")
    print("-" * 50)
    
    # Bullish trend
    trend1 = strategy.check_trend_filter(price=50000, ema50=49000, ema200=48000)
    print(f"   Price: 50000, EMA50: 49000, EMA200: 48000")
    print(f"   Trend: {trend1} (expected: bullish)")
    
    # Bearish trend
    trend2 = strategy.check_trend_filter(price=45000, ema50=46000, ema200=47000)
    print(f"   Price: 45000, EMA50: 46000, EMA200: 47000")
    print(f"   Trend: {trend2} (expected: bearish)")
    
    # Test 5: Position size calculation
    print("\n📊 Test 5: Position Size Calculation")
    print("-" * 50)
    
    position_size = strategy.calculate_position_size(
        entry_price=50000,
        stop_loss=49500,
        action='buy'
    )
    print(f"   Entry: $50,000, Stop Loss: $49,500")
    print(f"   Position Size: {position_size:.8f}")
    print(f"   Risk per share: $500")
    print(f"   Total risk (1% of $10,000): $100")
    print(f"   Calculated size: {position_size:.8f} units")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")


if __name__ == "__main__":
    test_signal_processing()

