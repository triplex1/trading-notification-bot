# Supremo Strategy - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Flask
```bash
venv\Scripts\activate
python -m pip install flask==3.0.0
```

### 2. Start Webhook Server
```bash
python webhook_server.py
```

You should see:
```
🚀 Starting Supremo Trading Bot Webhook Server
📡 Listening on 0.0.0.0:5000
🔗 Webhook URL: http://0.0.0.0:5000/webhook
```

### 3. Test the Webhook

Open another terminal and test:
```bash
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d "{\"ticker\":\"BTCUSDT\",\"action\":\"buy\",\"price\":\"45000\",\"trend_bias\":\"bullish\",\"timestamp\":\"2024-01-15T10:30:00\"}"
```

### 4. Configure TradingView

1. Add alert conditions to your Pine Script (see `tradingview_pinescript_example.txt`)
2. Create alert in TradingView
3. Set webhook URL: `http://your-server-ip:5000/webhook`
4. Use JSON message format from the example

### 5. Expose Your Server (for TradingView)

**Option A: ngrok (easiest for testing)**
```bash
ngrok http 5000
# Use the HTTPS URL in TradingView
```

**Option B: Deploy to cloud** (Heroku, Railway, etc.)

## 📋 Configuration

Add to `.env`:
```env
RISK_PER_TRADE=1.0
TOTAL_EQUITY=10000
WEBHOOK_PORT=5000
```

## ✅ Verification

Run the test:
```bash
python test_supremo.py
```

All tests should pass!

## 📚 Full Documentation

See [SUPREMO_SETUP.md](SUPREMO_SETUP.md) for complete details.

