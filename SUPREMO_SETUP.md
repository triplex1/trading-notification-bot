# Supremo All-In-One Strategy Integration Guide

This guide explains how to integrate the Supremo All-In-One trading strategy with your Trading Notification Bot.

## Overview

The Supremo strategy uses:
- **Trend Filter**: EMA 50 and EMA 200 to determine bullish/bearish bias
- **Entry Zones**: Monday Low (ML), Weekly Open (WO), Monday High (MH), Previous Week High (PWH)
- **Take Profit**: Next logical range level
- **Stop Loss**: 1 ATR or fixed percentage
- **Risk Management**: 1% risk per trade based on total equity

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Install new dependencies
python -m pip install -r requirements.txt
```

### 2. Configure Environment Variables

Add these to your `.env` file:

```env
# Risk Management
RISK_PER_TRADE=1.0          # Percentage of equity to risk per trade (default: 1%)
TOTAL_EQUITY=10000          # Your total trading equity
ATR_PERIOD=14               # ATR calculation period
ATR_MULTIPLIER=1.0          # ATR multiplier for stop loss
FIXED_SL_PERCENT=0          # Fixed SL % (0 = use ATR)

# Webhook Server
WEBHOOK_PORT=5000           # Port for webhook server
WEBHOOK_HOST=0.0.0.0        # Host (0.0.0.0 for all interfaces)
WEBHOOK_SECRET=your_secret  # Optional: Secret key for webhook security
```

### 3. Start the Webhook Server

```bash
# Activate virtual environment
venv\Scripts\activate

# Run webhook server
python webhook_server.py
```

The server will start on `http://localhost:5000` (or your configured port).

### 4. Configure TradingView Alerts

#### Step 1: Add Alert Conditions to Your Pine Script

Add these alert conditions to your TradingView Pine Script:

```pinescript
// Example Alert Logic for Supremo Strategy
longCondition = ta.crossover(close, emlive1) and close > emlive2
shortCondition = ta.crossunder(close, emlive1) and close < emlive2

// Long Entry at Monday Low or Weekly Open
longEntryML = close <= mondayLow and close > emlive1 and emlive1 > emlive2
longEntryWO = close <= weeklyOpen and close > emlive1 and emlive1 > emlive2

// Short Entry at Monday High or Previous Week High
shortEntryMH = close >= mondayHigh and close < emlive1 and emlive1 < emlive2
shortEntryPWH = close >= prevWeekHigh and close < emlive1 and emlive1 < emlive2

// Alert Conditions
alertcondition(longEntryML, title="Supremo Buy ML", message="{{ticker}}|buy|{{close}}|{{plot('Monday Low')}}|{{plot('Monday Mid')}}|bullish|{{timenow}}|ML")
alertcondition(longEntryWO, title="Supremo Buy WO", message="{{ticker}}|buy|{{close}}|{{plot('Weekly Open')}}|{{plot('Monday Mid')}}|bullish|{{timenow}}|WO")
alertcondition(shortEntryMH, title="Supremo Sell MH", message="{{ticker}}|sell|{{close}}|{{plot('Monday High')}}|{{plot('Monday Mid')}}|bearish|{{timenow}}|MH")
alertcondition(shortEntryPWH, title="Supremo Sell PWH", message="{{ticker}}|sell|{{close}}|{{plot('Previous Week High')}}|{{plot('Monday High')}}|bearish|{{timenow}}|PWH")
```

#### Step 2: Create Webhook Alert in TradingView

1. Go to your TradingView chart
2. Click the "Alert" button (bell icon)
3. Create a new alert
4. Select your alert condition (e.g., "Supremo Buy ML")
5. In the "Webhook URL" field, enter:
   ```
   http://your-server-ip:5000/webhook
   ```
   Or if using a service like ngrok:
   ```
   https://your-ngrok-url.ngrok.io/webhook
   ```
6. In the "Message" field, use the JSON format:

```json
{
  "ticker": "{{ticker}}",
  "action": "buy",
  "price": "{{close}}",
  "sl": "{{plot('Monday Low')}}",
  "tp": "{{plot('Monday Mid')}}",
  "trend_bias": "bullish",
  "timestamp": "{{timenow}}",
  "entry_level": "ML",
  "atr": "{{ta.atr(14)}}"
}
```

#### Step 3: Alternative - Simple Message Format

If your TradingView plan doesn't support JSON in webhooks, use a pipe-separated format:

```
{{ticker}}|buy|{{close}}|{{plot('Monday Low')}}|{{plot('Monday Mid')}}|bullish|{{timenow}}|ML
```

Then update `webhook_server.py` to parse this format.

## Webhook Payload Format

The webhook expects a JSON payload with the following fields:

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `ticker` | Yes | Trading symbol | `"BTCUSDT"` |
| `action` | Yes | Trade direction | `"buy"` or `"sell"` |
| `price` | Yes | Entry price | `"89876.50"` |
| `sl` | No | Stop loss price | `"89000.00"` |
| `tp` | No | Take profit price | `"90500.00"` |
| `trend_bias` | No | Trend direction | `"bullish"` or `"bearish"` |
| `timestamp` | No | Signal timestamp | `"2024-01-15T10:30:00"` |
| `entry_level` | No | Entry level identifier | `"ML"`, `"WO"`, `"MH"`, `"PWH"` |
| `atr` | No | ATR value for SL calculation | `"500.00"` |
| `secret` | No | Webhook secret (if configured) | `"your_secret"` |

## Strategy Logic

### Trend Filter
- **Bullish**: Price > EMA 50 > EMA 200
- **Bearish**: Price < EMA 50 < EMA 200

### Entry Conditions

**Long Entries:**
- Price touches/sweeps Monday Low (ML) OR Weekly Open (WO)
- Trend must be Bullish

**Short Entries:**
- Price touches/sweeps Monday High (MH) OR Previous Week High (PWH)
- Trend must be Bearish

### Take Profit Levels

- **Long from ML/WO**: TP1 = Monday Mid, TP2 = Monday High
- **Short from MH/PWH**: TP1 = Monday Mid (or Monday High), TP2 = Monday Low (or Monday Mid)

### Stop Loss

- Uses 1 ATR (if provided) or fixed percentage
- Long: Entry - (ATR × multiplier)
- Short: Entry + (ATR × multiplier)

### Risk Management

- Position size calculated to risk 1% of total equity
- Formula: `Position Size = (Total Equity × Risk %) / (Entry Price - Stop Loss)`

### Deduplication

- Signals within the same 15-minute candle are ignored
- Prevents duplicate trades from the same setup

## Testing

### Test the Webhook Server

```bash
# Start the server
python webhook_server.py

# In another terminal, test with curl
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTCUSDT",
    "action": "buy",
    "price": "89876.50",
    "sl": "89000.00",
    "tp": "90500.00",
    "trend_bias": "bullish",
    "timestamp": "2024-01-15T10:30:00",
    "entry_level": "ML"
  }'
```

### Expected Response

```json
{
  "status": "success",
  "signal": {
    "ticker": "BTCUSDT",
    "action": "buy",
    "entry_price": 89876.5,
    "stop_loss": 89000.0,
    "tp1": 90500.0,
    "tp2": 91000.0,
    "position_size": 0.11428571,
    "risk_amount": 100.0,
    ...
  }
}
```

## Exposing Your Webhook Server

### Option 1: ngrok (Recommended for Testing)

```bash
# Install ngrok: https://ngrok.com/
ngrok http 5000

# Use the provided HTTPS URL in TradingView
```

### Option 2: Cloud Deployment

Deploy to services like:
- Heroku
- Railway
- DigitalOcean
- AWS EC2

### Option 3: Port Forwarding

If running on a VPS, configure firewall to allow port 5000.

## Troubleshooting

### Webhook Not Receiving Signals

1. Check server is running: `curl http://localhost:5000/health`
2. Verify TradingView webhook URL is correct
3. Check server logs for incoming requests
4. Verify JSON payload format matches expected structure

### Duplicate Signals

- Deduplication window is 15 minutes
- Same ticker signals within this window are ignored
- Adjust `deduplication_window` in `supremo_strategy.py` if needed

### Position Size Calculation Issues

- Verify `TOTAL_EQUITY` is set correctly
- Check that stop loss is valid (not equal to entry price)
- Ensure `RISK_PER_TRADE` is a percentage (e.g., 1.0 for 1%)

## Integration with Existing Bot

The Supremo strategy runs alongside your existing price monitoring bot. You can:

1. Run both simultaneously:
   ```bash
   # Terminal 1: Price monitoring bot
   python main.py
   
   # Terminal 2: Webhook server
   python webhook_server.py
   ```

2. Or integrate them into a single script (see `supremo_integrated.py`)

## Next Steps

- Configure your TradingView alerts
- Test with paper trading first
- Monitor notifications to verify signals
- Adjust risk parameters based on your strategy
- Consider adding order execution if using an exchange API

