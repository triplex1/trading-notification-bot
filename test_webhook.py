"""
Test script for webhook server.
Tests the webhook endpoint with sample TradingView payloads.
"""

import sys
import time
import requests
import threading
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

from webhook_server import app


def test_webhook_server():
    """Test the webhook server with sample requests."""
    print("🧪 Testing Webhook Server")
    print("=" * 50)
    
    # Start server in a thread
    def run_server():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Starting webhook server...")
    time.sleep(3)
    
    # Test 1: Health check
    print("\n📊 Test 1: Health Check")
    print("-" * 50)
    try:
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: Root endpoint
    print("\n📊 Test 2: Root Endpoint")
    print("-" * 50)
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Webhook with valid signal
    print("\n📊 Test 3: Webhook - Valid Buy Signal")
    print("-" * 50)
    
    payload = {
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
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/webhook',
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook request successful")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            if 'signal' in data:
                signal = data['signal']
                print(f"   Ticker: {signal.get('ticker')}")
                print(f"   Action: {signal.get('action')}")
                print(f"   Entry: ${signal.get('entry_price'):,.2f}")
                print(f"   Position Size: {signal.get('position_size')}")
        else:
            print(f"❌ Webhook request failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Webhook request error: {e}")
    
    # Test 4: Webhook with invalid payload
    print("\n📊 Test 4: Webhook - Invalid Payload")
    print("-" * 50)
    
    invalid_payload = {
        "ticker": "BTCUSDT"
        # Missing required fields
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/webhook',
            json=invalid_payload,
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Invalid payload correctly rejected")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Webhook with duplicate signal (deduplication)
    print("\n📊 Test 5: Webhook - Duplicate Signal (Deduplication)")
    print("-" * 50)
    
    duplicate_payload = payload.copy()
    
    try:
        # First request
        response1 = requests.post(
            'http://127.0.0.1:5000/webhook',
            json=payload,
            timeout=10
        )
        
        # Second request (duplicate)
        response2 = requests.post(
            'http://127.0.0.1:5000/webhook',
            json=duplicate_payload,
            timeout=10
        )
        
        if response2.status_code == 400:
            print("✅ Duplicate signal correctly ignored")
        else:
            print(f"⚠️  Duplicate signal status: {response2.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Webhook server tests completed!")
    print("\n💡 Note: Server will continue running in background.")
    print("   Press Ctrl+C to stop if needed.")


if __name__ == "__main__":
    test_webhook_server()

