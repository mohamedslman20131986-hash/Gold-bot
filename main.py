import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

last_price = None

def get_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url)
        data = response.json()
        ounce_price = data["price"]

        # تحويل الى غرام
        gram_price_usd = ounce_price / 31.1035

        return gram_price_usd
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
        global last_price
        
        # تحويل للعراقي (تقريباً 1300 دينار لكل دولار)
        price_iq = price * 1300

        # تحديد الاتجاه
        if last_price is None:
            trend = "➖ أول تحديث"
        elif price > last_price:
            trend = "🔺 صاعد"
        elif price < last_price:
            trend = "🔻 نازل"
        else:
            trend = "⏸️ ثابت"

        # منع التكرار
        if price != last_price:
            message = f"""💰 سعر الذهب الآن:

🔸 {price:.2f} دولار / غرام
🔸 {int(price_iq):,} دينار عراقي

📊 الحالة: {trend}
"""
            send_telegram_message(message)

            last_price = price

    else:
        send_telegram_message("❌ فشل في جلب السعر")

    time.sleep(60)
