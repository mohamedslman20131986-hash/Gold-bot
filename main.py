import requests
import time
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

URL = "https://goldliveksa.com/gold-prices-iraq"  # صفحة بها السعر المحلي

def get_gold_price_iraq():
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        
        # استخراج سعر الجرام عيار 21 من الصفحة
        price_tag = soup.find("td", text="عيار 21").find_next_sibling("td")
        price_iqd = price_tag.text.strip().replace(",", "").split()[0]
        
        return int(price_iqd)
    except Exception as e:
        print("Error:", e)
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    requests.post(url, data=data)

while True:
    price = get_gold_price_iraq()
    
    if price:
        message = f"💰 سعر الذهب في العراق الآن:\n📊 1 غرام عيار 21 ≈ {price:,} د.ع"
    else:
        message = "❌ فشل في جلب سعر الذهب من المصدر المحلي"
    
    send_telegram_message(message)
    
    time.sleep(60)
