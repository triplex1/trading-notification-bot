"""
Exchange API module for fetching cryptocurrency prices.
Supports multiple exchanges: Binance, Coinbase, etc.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_binance_price(symbol):
    """
    Fetch current price from Binance API.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Current price as float, or None if error
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {'symbol': symbol}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"Binance API error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing Binance response: {e}")
        return None


def get_coinbase_price(symbol):
    """
    Fetch current price from Coinbase API.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTC-USD', 'ETH-USD')
        
    Returns:
        Current price as float, or None if error
    """
    try:
        url = f"https://api.coinbase.com/v2/exchange-rates"
        params = {'currency': symbol.split('-')[0]}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        base_currency = symbol.split('-')[1] if '-' in symbol else 'USD'
        return float(data['data']['rates'][base_currency])
    except requests.exceptions.RequestException as e:
        print(f"Coinbase API error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing Coinbase response: {e}")
        return None


def get_current_price(symbol):
    """
    Get current price from the configured exchange.
    
    Args:
        symbol: Trading pair symbol
        
    Returns:
        Current price as float, or None if error
    """
    exchange = os.getenv('EXCHANGE', 'binance').lower()
    
    if exchange == 'binance':
        return get_binance_price(symbol)
    elif exchange == 'coinbase':
        # Convert symbol format if needed (BTCUSDT -> BTC-USD)
        if '-' not in symbol:
            base = symbol.replace('USDT', '').replace('USD', '')
            symbol = f"{base}-USD"
        return get_coinbase_price(symbol)
    else:
        print(f"Unsupported exchange: {exchange}")
        print("Defaulting to Binance...")
        return get_binance_price(symbol)

