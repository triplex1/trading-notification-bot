# Trading Notification Bot

A Python bot that monitors cryptocurrency prices and sends notifications when price thresholds are crossed.

## Features

- 📊 Real-time price monitoring from multiple exchanges (Binance, Coinbase)
- 🔔 Multi-channel notifications (Telegram, Email, Discord)
- ⚙️ Configurable price thresholds
- 🔄 Automatic retry on errors
- 📈 Price change tracking

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

## Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| `SYMBOL` | Trading pair to monitor | `BTCUSDT`, `ETHUSDT` |
| `EXCHANGE` | Exchange to use | `binance`, `coinbase` |
| `PRICE_THRESHOLD_ABOVE` | Alert when price goes above this | `50000` |
| `PRICE_THRESHOLD_BELOW` | Alert when price goes below this | `45000` |
| `CHECK_INTERVAL` | Seconds between price checks | `60` |

## Supported Exchanges

- **Binance**: Use symbols like `BTCUSDT`, `ETHUSDT`
- **Coinbase**: Use symbols like `BTC-USD`, `ETH-USD`

## Troubleshooting

- **No notifications sent**: Check that at least one notification method is properly configured in `.env`
- **API errors**: Verify your internet connection and that the exchange API is accessible
- **Import errors**: Make sure virtual environment is activated and dependencies are installed

## License

MIT

