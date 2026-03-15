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
    return "Lordum, botunuz 7/24 uyanık!"

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

# --- BOT KURULUMU ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

async def aternos_baglan_async():
    global sunucu
    if not ATERNOS_SESSION:
        print("❌ HATA: ATERNOS_SESSION bulunamadı!")
        return

    try:
        print("⏳ Aternos'a bağlanılıyor...")
        # YENİ SİSTEM: login_with_session yerine doğrudan Client içinde session veriyoruz
        atclient = Client(ATERNOS_SESSION) 
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print(f"✅ Başarıyla bağlanıldı: {sunucu.address}")
    except Exception as e:
        print(f"❌ Aternos Hatası: {e}")
        sunucu = None

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!sunucuac emrini bekliyor"))
    print(f"🚀 {bot.user} DİSCORD'A GİRDİ!")
    await aternos_baglan_async()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    if sunucu is None:
        await aternos_baglan_async()
        
    if sunucu is None:
        await ctx.send("❌ Lordum, Aternos anahtarı (Session ID) hatalı! Render panelinden güncelleyin.")
        return
        
    await ctx.send("Emredersiniz yüce efendim! Sunucu şalteri indiriliyor...")
    try:
        # Sunucuyu dondurmadan başlat
        await asyncio.to_thread(sunucu.start)
        await ctx.send("✅ Karanlık Lord uyanıyor! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

@bot.command()
async def baglan(ctx):
    await ctx.send("⏳ Bağlantı tazeleniyor...")
    await aternos_baglan_async()
    if sunucu:
        await ctx.send("✅ Bağlantı kuruldu!")
    else:
        await ctx.send("❌ Başarısız. Session ID'yi kontrol edin.")

if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ HATA: DISCORD_TOKEN bulunamadı!")
