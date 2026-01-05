"""
Notification module for sending alerts via various channels.
Supports: Telegram, Email, Discord, etc.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_notification(message):
    """
    Send notification via Telegram bot.
    
    Args:
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not telegram_token or not chat_id:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Telegram notification error: {e}")
        return False


def send_email_notification(message):
    """
    Send notification via Email.
    
    Args:
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    smtp_server = os.getenv('EMAIL_SMTP_SERVER')
    smtp_port = int(os.getenv('EMAIL_PORT', '587'))
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_to = os.getenv('EMAIL_TO', email_user)
    
    if not all([smtp_server, email_user, email_password]):
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_to
        msg['Subject'] = "Trading Bot Alert"
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email notification error: {e}")
        return False


def send_discord_notification(message):
    """
    Send notification via Discord webhook.
    
    Args:
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        return False
    
    try:
        payload = {'content': message}
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Discord notification error: {e}")
        return False


def send_notification(message):
    """
    Send notification via all configured channels.
    
    Args:
        message: Message text to send
    """
    success_count = 0
    
    # Try Telegram
    if send_telegram_notification(message):
        success_count += 1
    
    # Try Email
    if send_email_notification(message):
        success_count += 1
    
    # Try Discord
    if send_discord_notification(message):
        success_count += 1
    
    # If no notification method is configured, just print
    if success_count == 0:
        print(f"⚠️  No notification method configured. Message: {message}")

