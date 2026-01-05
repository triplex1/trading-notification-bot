# Telegram Notification Setup Guide

## Step-by-Step Instructions

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat with BotFather
3. Send the command: `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "My Trading Bot")
   - Choose a username for your bot (must end with "bot", e.g., "my_trading_bot")
5. BotFather will give you a **token** that looks like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **Copy this token** - you'll need it for your `.env` file

### Step 2: Get Your Chat ID

1. Open Telegram and search for **@userinfobot**
2. Start a chat with @userinfobot
3. It will reply with your user information including your **Chat ID**
4. **Copy the Chat ID** (it's a number like `123456789`)

### Step 3: Configure Your .env File

1. Create a file named `.env` in your project root directory
2. Copy this template and fill in your values:

```env
# Trading Configuration
SYMBOL=BTCUSDT
EXCHANGE=binance
PRICE_THRESHOLD_ABOVE=50000
PRICE_THRESHOLD_BELOW=45000
CHECK_INTERVAL=60

# Telegram Notification
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

3. Replace:
   - `your_telegram_bot_token_here` with the token from BotFather
   - `your_telegram_chat_id_here` with your Chat ID from @userinfobot

### Step 4: Test Your Setup

1. Make sure your `.env` file is saved
2. Run the bot:
   ```bash
   python main.py
   ```
3. The bot will send a test notification when price thresholds are crossed

## Quick Links

- [@BotFather](https://t.me/botfather) - Create your bot
- [@userinfobot](https://t.me/userinfobot) - Get your Chat ID

## Troubleshooting

- **Bot not responding?** Make sure you've started a chat with your bot first (send `/start` to your bot)
- **Token not working?** Double-check you copied the entire token from BotFather
- **Chat ID wrong?** Make sure you're using the number from @userinfobot, not your username

