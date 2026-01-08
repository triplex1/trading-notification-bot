"""
Integrated Supremo Trading Bot
Combines webhook server with optional price monitoring.
"""

import os
import sys
import threading
import time
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

load_dotenv()


def run_webhook_server():
    """Run the webhook server in a separate thread."""
    from webhook_server import app
    port = int(os.getenv('WEBHOOK_PORT', '5000'))
    host = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    
    print("🚀 Starting Webhook Server...")
    app.run(host=host, port=port, debug=False, use_reloader=False)


def run_price_monitor():
    """Run the price monitoring bot in a separate thread."""
    from main import TradingBot
    
    print("📊 Starting Price Monitor...")
    bot = TradingBot()
    bot.run()


def main():
    """Main function to run integrated bot."""
    print("=" * 50)
    print("🤖 Supremo Trading Bot - Integrated Mode")
    print("=" * 50)
    
    # Check which services to run
    run_webhook = os.getenv('ENABLE_WEBHOOK', 'true').lower() == 'true'
    run_monitor = os.getenv('ENABLE_MONITOR', 'false').lower() == 'true'
    
    threads = []
    
    # Start webhook server
    if run_webhook:
        webhook_thread = threading.Thread(target=run_webhook_server, daemon=True)
        webhook_thread.start()
        threads.append(webhook_thread)
        print("✅ Webhook server started")
        time.sleep(2)  # Give server time to start
    
    # Start price monitor
    if run_monitor:
        monitor_thread = threading.Thread(target=run_price_monitor, daemon=True)
        monitor_thread.start()
        threads.append(monitor_thread)
        print("✅ Price monitor started")
    
    if not threads:
        print("⚠️  No services enabled. Set ENABLE_WEBHOOK or ENABLE_MONITOR in .env")
        return
    
    print("-" * 50)
    print("🟢 All services running. Press Ctrl+C to stop.")
    print("-" * 50)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")


if __name__ == "__main__":
    main()

