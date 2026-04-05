import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url)
        data = response.json()
        price = data["price"]
        return price
    except:
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    requests.post(url, data=data)

while True:
    price = get_gold_price()
    
    if price:
        message = f"💰 سعر الذهب الآن:\n{price} دولار للأونصة"
    else:
        message = "❌ فشل في جلب السعر"

    send_telegram_message(message)
    time.sleep(60)
