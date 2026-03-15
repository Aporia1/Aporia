import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os
import asyncio

# --- 7/24 BEKÇİ ---
app = Flask('')
@app.route('/')
def home(): return "Online!"
def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- ANAHTARLAR ---
TOKEN = os.getenv("DISCORD_TOKEN")
SESSION = os.getenv("ATERNOS_SESSION")

# --- BOT ---
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sunucu = None

async def baglan():
    global sunucu
    try:
        # python-aternos 2.x sürümü için en sağlam giriş yöntemi
        at = Client(SESSION)
        sunucu = at.account.list_servers()[0]
        print(f"✅ Bağlantı kuruldu: {sunucu.address}")
    except Exception as e:
        print(f"❌ Hata: {e}")
        sunucu = None

@bot.event
async def on_ready():
    print(f"🚀 {bot.user} ONLINE!")
    await baglan()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None: await baglan()
    if sunucu is None:
        await ctx.send("❌ Aternos bağlantısı başarısız. Session ID yenileyin.")
        return
    await ctx.send("⏳ Şalter indiriliyor...")
    try:
        await asyncio.to_thread(sunucu.start)
        await ctx.send("✅ Sunucu açılıyor!")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
