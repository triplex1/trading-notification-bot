# Trading Notification Bot

A Python bot that monitors cryptocurrency prices and sends notifications when price thresholds are crossed.

## Features

- 📊 Real-time price monitoring from multiple exchanges (Binance, Coinbase)
- 🔔 Multi-channel notifications (Telegram, Email, Discord)
- ⚙️ Configurable price thresholds
- 🔄 Automatic retry on errors
- 📈 Price change tracking
- 🎯 **Supremo All-In-One Strategy Integration** - Advanced algorithmic trading with webhook support
- 📡 **TradingView Webhook Server** - Receive and process alerts from TradingView
- 💰 **Risk Management** - Automatic position sizing based on 1% risk per trade

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Install packages
python -m pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your settings:

```bash
copy .env.example .env
```

Edit `.env` with your configuration:
- Set `SYMBOL` to the trading pair you want to monitor (e.g., BTCUSDT, ETHUSDT)
- Set price thresholds (`PRICE_THRESHOLD_ABOVE` and `PRICE_THRESHOLD_BELOW`)
- Configure at least one notification method (Telegram, Email, or Discord)

### 3. Get Notification Credentials

#### Telegram (Recommended)
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token to `TELEGRAM_BOT_TOKEN`
4. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
5. Add chat ID to `TELEGRAM_CHAT_ID`

#### Email
- For Gmail: Use an [App Password](https://support.google.com/accounts/answer/185833)
- Add SMTP settings to `.env`

#### Discord
1. Go to your Discord server settings
2. Integrations → Webhooks → New Webhook
3. Copy webhook URL to `DISCORD_WEBHOOK_URL`

## Usage

### Basic Price Monitoring

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the bot
python main.py
```

The bot will:
- Monitor the configured symbol every 60 seconds (or your `CHECK_INTERVAL`)
- Send alerts when price crosses your thresholds
- Display current price and changes in the console

Press `Ctrl+C` to stop the bot.

### Supremo Strategy with TradingView Webhooks

```bash
# Activate virtual environment
venv\Scripts\activate

# Run webhook server for TradingView alerts
python webhook_server.py
```

Or run integrated mode (webhook + price monitor):

```bash
python supremo_integrated.py
```

**See [SUPREMO_SETUP.md](SUPREMO_SETUP.md) for complete setup instructions.**

## Configuration Options

### Basic Price Monitoring

| Variable | Description | Example |
|----------|-------------|---------|
| `SYMBOL` | Trading pair to monitor | `BTCUSDT`, `ETHUSDT` |
| `EXCHANGE` | Exchange to use | `binance`, `coinbase` |
| `PRICE_THRESHOLD_ABOVE` | Alert when price goes above this | `50000` |
| `PRICE_THRESHOLD_BELOW` | Alert when price goes below this | `45000` |
| `CHECK_INTERVAL` | Seconds between price checks | `60` |

### Supremo Strategy

| Variable | Description | Example |
|----------|-------------|---------|
| `RISK_PER_TRADE` | Percentage of equity to risk per trade | `1.0` (1%) |
| `TOTAL_EQUITY` | Total trading equity | `10000` |
| `ATR_PERIOD` | ATR calculation period | `14` |
| `ATR_MULTIPLIER` | ATR multiplier for stop loss | `1.0` |
| `FIXED_SL_PERCENT` | Fixed SL % (0 = use ATR) | `0` |
| `WEBHOOK_PORT` | Port for webhook server | `5000` |
| `WEBHOOK_HOST` | Host for webhook server | `0.0.0.0` |
| `WEBHOOK_SECRET` | Optional secret for webhook security | `your_secret` |
| `ENABLE_WEBHOOK` | Enable webhook server in integrated mode | `true` |
| `ENABLE_MONITOR` | Enable price monitor in integrated mode | `false` |

## Supported Exchanges

- **Binance**: Use symbols like `BTCUSDT`, `ETHUSDT`
- **Coinbase**: Use symbols like `BTC-USD`, `ETH-USD`

## Advanced Features

### Supremo All-In-One Strategy

The bot includes a complete implementation of the Supremo All-In-One trading strategy:

- **Trend Filter**: EMA 50/200 based trend detection
- **Entry Zones**: Monday Low/High, Weekly Open, Previous Week High
- **Take Profit**: Automatic TP1/TP2 calculation
- **Stop Loss**: ATR-based or fixed percentage
- **Risk Management**: 1% risk per trade with automatic position sizing
- **Deduplication**: Prevents duplicate signals within 15-minute windows

**Full documentation**: See [SUPREMO_SETUP.md](SUPREMO_SETUP.md)

### TradingView Integration

Connect your TradingView alerts to the bot via webhook:

1. Set up webhook server: `python webhook_server.py`
2. Configure TradingView alerts with webhook URL
3. Receive and process signals automatically

## Troubleshooting

- **No notifications sent**: Check that at least one notification method is properly configured in `.env`
- **API errors**: Verify your internet connection and that the exchange API is accessible
- **Import errors**: Make sure virtual environment is activated and dependencies are installed
- **Webhook not receiving signals**: Check server is running, verify TradingView webhook URL, check firewall settings
- **Duplicate signals**: Signals within 15-minute windows are automatically deduplicated

## License

MIT

