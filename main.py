import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os

# --- 7/24 UYANIK TUTMA SİSTEMİ ---
app = Flask('')

@app.route('/')
def home():
    return "Lordum, botunuz 7/24 görev başında!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- GİZLİ ANAHTARLAR (RENDER ENVIRONMENT'DAN ÇEKER) ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

def aternos_baglan():
    global sunucu
    try:
        atclient = Client()
        atclient.login_with_session(ATERNOS_SESSION)
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print("✅ Aternos bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ Aternos hatası: {e}")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} uyanışını tamamladı!")
    aternos_baglan()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        aternos_baglan()
        if sunucu is None:
            await ctx.send("❌ Aternos bağlantısı kurulamadı lordum!")
            return
        
    await ctx.send("Emredersiniz yüce efendim! Sunucu şalteri indiriliyor...")
    try:
        sunucu.start()
        await ctx.send("✅ Karanlık Lord uyanıyor! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ HATA: DISCORD_TOKEN bulunamadı!")
