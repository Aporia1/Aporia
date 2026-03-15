import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os
import asyncio

# --- 7/24 BEKÇİ SİSTEMİ ---
app = Flask('')
@app.route('/')
def home():
    return "Bot Online!"

def run():
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
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

async def aternos_baglan_async():
    global sunucu
    if not ATERNOS_SESSION:
        print("❌ HATA: ATERNOS_SESSION bulunamadı!")
        return
    try:
        print("⏳ Aternos kalesine sızılıyor...")
        # YENİ SİSTEM: login_with_session tamamen kalktı.
        atclient = Client(session=ATERNOS_SESSION) 
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print(f"✅ Bağlantı BAŞARILI: {sunucu.address}")
    except Exception as e:
        print(f"❌ Aternos Hatası: {e}")
        sunucu = None

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!sunucuac emrini bekliyor"))
    print(f"🚀 {bot.user} ONLINE!")
    await aternos_baglan_async()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        await aternos_baglan_async()
    if sunucu is None:
        await ctx.send("❌ Bağlantı kurulamadı. Render panelinden Session ID'yi güncelleyin.")
        return
    await ctx.send("Emredersiniz yüce efendim! Şalter indiriliyor...")
    try:
        await asyncio.to_thread(sunucu.start)
        await ctx.send("✅ Sunucu açılıyor!")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ HATA: DISCORD_TOKEN bulunamadı!")
