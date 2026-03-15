import discord
from discord.ext import commands
from python_aternos import Client
from flask import Flask
from threading import Thread
import os

# --- KALP ATIŞI SİSTEMİ (BOTUN UYUMAMASI İÇİN) ---
app = Flask('')

@app.route('/')
def home():
    return "Yüce Efendi'nin botu 7/24 aktif ve görevde!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- YÜCE EFENDİ'NİN GİZLİ ANAHTARLARI (YENİLERİYLE DEĞİŞTİRİN!) ---
DISCORD_TOKEN = "YENİ_TOKEN_BURAYA"
ATERNOS_SESSION = "YENİ_SESSION_ID_BURAYA"

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

# --- ATERNOS'A SIZMA SİSTEMİ ---
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
    print(f"✅ {bot.user} göreve hazır!")
    aternos_baglan()

@bot.command()
async def sunucuac(ctx):
    if sunucu is None:
        aternos_baglan()
        if sunucu is None:
            await ctx.send("❌ Aternos bağlantısı kurulamadı yüce efendim!")
            return
        
    await ctx.send("Yüce efendimin emri alındı! Şalter indiriliyor...")
    try:
        sunucu.start()
        await ctx.send("✅ Şalter indirildi! Karanlık Lord uyanıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata oluştu: {e}")

# --- BOTU ÖLÜMSÜZLEŞTİR VE BAŞLAT ---
keep_alive()
bot.run(DISCORD_TOKEN)
