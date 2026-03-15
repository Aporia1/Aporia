import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os
import asyncio

# --- KALP ATIŞI SİSTEMİ (RENDER İÇİN) ---
app = Flask('')

@app.route('/')
def home():
    return "Lordum, botunuz 7/24 görev başında!"

def run():
    # Render'ın botu görmesi için portu 10000 yapalım, daha garantidir.
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- GİZLİ ANAHTARLAR (RENDER ENVIRONMENT'DAN) ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

async def aternos_baglan_async():
    global sunucu
    try:
        # Aternos işlemini botu dondurmadan (async) yapalım
        loop = asyncio.get_event_loop()
        atclient = Client()
        await loop.run_in_executor(None, lambda: atclient.login_with_session(ATERNOS_SESSION))
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print("✅ Aternos bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ Aternos hatası: {e}")

@bot.event
async def on_ready():
    # BOTUN ONLINE OLDUĞUNU İSPATLAMAK İÇİN DURUM EKLEYELİM
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Karanlık Lord'u"))
    print(f"✅ {bot.user} uyanışını tamamladı ve şu an ONLINE!")
    await aternos_baglan_async()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        await aternos_baglan_async()
        if sunucu is None:
            await ctx.send("❌ Aternos bağlantısı kurulamadı lordum!")
            return
        
    await ctx.send("Emredersiniz yüce efendim! Sunucu şalteri indiriliyor...")
    try:
        # Sunucu başlatma işlemini dondurmadan yapalım
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, sunucu.start)
        await ctx.send("✅ Karanlık Lord uyanıyor! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            print(f"❌ BOT LOGİN HATASI: {e}")
    else:
        print("❌ HATA: Render panelinde DISCORD_TOKEN bulunamadı!")
