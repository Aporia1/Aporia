import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os

# --- KALP ATIŞI SİSTEMİ (BOTUN UYUMAMASI İÇİN) ---
# Render/UptimeRobot bu adrese bakınca botu canlı sanacak.
app = Flask('')

@app.route('/')
def home():
    return "Yüce Efendi'nin botu 7/24 aktif ve görevde!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- GİZLİ ANAHTARLAR (GÜVENLİ YÖNTEM) ---
# GitHub'ın engellememesi için token'ları koda yazmıyoruz. 
# Render panelindeki "Environment Variables" kısmından okuyacak.
DISCORD_TOKEN = os.getenv("MTQ4MjUxMjI4MDA3OTA0NDY3MA.GUf18P.MDR0oqReRxuphpRrXbpzxo_GrWJgIGLoTV3gEo")
ATERNOS_SESSION = os.getenv("jgcjmDURpvROjkc2yH9AeO9tHNM91Ui2LVJ3ob4K0nf4w6ozlXM5uYIVwclN3lvPcTtzaq4LeOVJCcRlnltXnKZ1OE9ZscOETFWI")

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

# --- ATERNOS BAĞLANTI SİSTEMİ ---
def aternos_baglan():
    global sunucu
    try:
        atclient = Client()
        atclient.login_with_session(ATERNOS_SESSION)
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0] # Hesaptaki ilk sunucuyu seçer
        print("✅ Aternos bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ Aternos bağlantı hatası: {e}")

# --- OLAYLAR ---
@bot.event
async def on_ready():
    print(f"✅ Yüce Efendi'nin emrindeki {bot.user} göreve hazır!")
    aternos_baglan()

# --- SUNUCU AÇMA KOMUTU ---
@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        aternos_baglan()
        if sunucu is None:
            await ctx.send("❌ Aternos bağlantısı kurulamadı! Lütfen Render'daki Session ID'yi kontrol edin.")
            return
        
    await ctx.send("Yüce efendimin emri alındı! Aternos şalteri indiriliyor...")
    try:
        sunucu.start()
        await ctx.send("✅ Şalter indirildi! Sunucu açılıyor, Karanlık Lord uyanıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata oluştu (Sunucu zaten açık veya sıra bekliyor olabilir): {e}")

# --- BOTU ÖLÜMSÜZLEŞTİR VE BAŞLAT ---
if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ HATA: DISCORD_TOKEN bulunamadı! Render panelinden eklemeyi unutmayın.")
