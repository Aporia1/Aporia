import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os
import asyncio

# --- RENDER PORT AYARI ---
# Render'ın botu kapatmaması için gerekli olan hayat öpücüğü
app = Flask('')

@app.route('/')
def home():
    return "Lordum, botunuz 7/24 uyanık!"

def run():
    # Render'ın atadığı portu otomatik alır, yoksa 10000 kullanır.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- GİZLİ ANAHTARLAR ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

# --- BOT AYARLARI ---
intents = discord.Intents.all() # Tüm kapıları zorla açıyoruz!
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

async def aternos_baglan_async():
    global sunucu
    try:
        print("⏳ Aternos'a bağlanılıyor...")
        atclient = Client()
        # Aternos'u ana motoru yormadan bağlayalım
        await asyncio.to_thread(atclient.login_with_session, ATERNOS_SESSION)
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print("✅ Aternos bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ Aternos Hatası: {e}")

@bot.event
async def on_ready():
    # Botun uyanık olduğunu Discord'da ispatlayalım
    await bot.change_presence(activity=discord.Game(name="!sunucuac emrini bekliyor"))
    print(f"🚀 {bot.user} DİSCORD'A GİRİŞ YAPTI!")
    await aternos_baglan_async()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        await aternos_baglan_async()
        if sunucu is None:
            await ctx.send("❌ Aternos kalesi düşmüş yüce efendim! Bağlantı yok.")
            return
        
    await ctx.send("Emredersiniz yüce efendim! Aternos şalterini indiriyorum...")
    try:
        await asyncio.to_thread(sunucu.start)
        await ctx.send("✅ Şalter indirildi! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

# --- OPERASYON BAŞLASIN ---
if __name__ == "__main__":
    keep_alive() # Web bekçisini uyandır
    if DISCORD_TOKEN:
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            print(f"❌ BOT ÇALIŞTIRILAMADI: {e}")
    else:
        print("❌ KRİTİK HATA: DISCORD_TOKEN bulunamadı!")
