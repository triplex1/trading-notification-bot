"""
Webhook Server for TradingView Alerts
Receives JSON payloads from TradingView and processes them through Supremo strategy.
"""

import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supremo_strategy import SupremoStrategy
from notification import send_notification

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

app = Flask(__name__)
strategy = SupremoStrategy()

# Webhook secret for security (optional)
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint for TradingView alerts.
    
    Expected JSON payload:
    {
        "ticker": "{{ticker}}",
        "action": "buy/sell",
        "price": "{{close}}",
        "sl": "{{plot('Monday Low')}}",
        "tp": "{{plot('Monday Mid')}}",
        "trend_bias": "bullish/bearish",
        "timestamp": "{{timenow}}",
        "entry_level": "ML/WO/MH/PWH",
        "atr": "{{atr_value}}"
    }
    """
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        # Optional: Verify webhook secret
        if WEBHOOK_SECRET:
            received_secret = data.get('secret')
            if received_secret != WEBHOOK_SECRET:
                print("⚠️  Invalid webhook secret")
                return jsonify({'error': 'Invalid secret'}), 401
        
        # Log received signal
        print(f"\n📥 Received signal: {data.get('ticker')} - {data.get('action')}")
        
        # Process signal through strategy
        signal = strategy.process_signal(data)
        
        if not signal:
            return jsonify({'error': 'Signal processing failed or duplicate'}), 400
        
        # Format and send notification
        message = strategy.format_signal_message(signal)
        send_notification(message)
        
        # Log success
        print(f"✅ Signal processed and notification sent")
        print(f"   {signal['ticker']} {signal['action'].upper()} @ ${signal['entry_price']:,.2f}")
        
        # Return success response
        return jsonify({
            'status': 'success',
            'signal': signal
        }), 200
        
    except Exception as e:
        error_msg = f"Error processing webhook: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({'error': error_msg}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Supremo Trading Bot Webhook Server'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with instructions."""
    return jsonify({
        'service': 'Supremo Trading Bot Webhook Server',
        'endpoints': {
            '/webhook': 'POST - Receive TradingView alerts',
            '/health': 'GET - Health check'
        },
        'usage': 'Send POST requests to /webhook with TradingView alert JSON payload'
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('WEBHOOK_PORT', '5000'))
    host = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    
    print("🚀 Starting Supremo Trading Bot Webhook Server")
    print(f"📡 Listening on {host}:{port}")
    print(f"🔗 Webhook URL: http://{host}:{port}/webhook")
    print("-" * 50)
    
    # Run Flask app
    app.run(host=host, port=port, debug=False)

