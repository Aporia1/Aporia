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

# --- ANAHTARLAR ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

# --- BOT KURULUMU ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

sunucu = None

async def aternos_baglan_async():
    global sunucu
    if not ATERNOS_SESSION:
        print("❌ HATA: ATERNOS_SESSION Render panelinde bulunamadı!")
        return

    try:
        print("⏳ Aternos kalesine sızılıyor...")
        atclient = Client()
        # Aternos login işlemini ayrı bir kanalda yapalım
        await asyncio.to_thread(atclient.login_with_session, ATERNOS_SESSION)
        aternos_hesap = atclient.account
        sunucu = aternos_hesap.list_servers()[0]
        print(f"✅ Aternos bağlantısı başarılı: {sunucu.address}")
    except Exception as e:
        print(f"❌ Aternos Bağlantı Hatası: {e}")
        sunucu = None

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!sunucuac emrini bekliyor"))
    print(f"🚀 {bot.user} Discord'a giriş yaptı!")
    await aternos_baglan_async()

@bot.command()
async def sunucuac(ctx):
    global sunucu
    # Eğer bağlantı kopmuşsa tekrar denetelim
    if sunucu is None:
        await ctx.send("⏳ Bağlantı yoktu, tekrar sızmaya çalışıyorum...")
        await aternos_baglan_async()
        
    if sunucu is None:
        await ctx.send("❌ Lordum, Aternos anahtarınız (Session ID) hatalı veya süresi dolmuş! Lütfen Render panelinden güncelleyin.")
        return
        
    await ctx.send("Emredersiniz yüce efendim! Sunucu şalteri indiriliyor...")
    try:
        await asyncio.to_thread(sunucu.start)
        await ctx.send("✅ Karanlık Lord uyanıyor! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"❌ Şalter takıldı (Hata): {e}")

# Bağlantıyı manuel tazeleme komutu
@bot.command()
async def baglan(ctx):
    await ctx.send("⏳ Aternos'a yeniden bağlanılıyor...")
    await aternos_baglan_async()
    if sunucu:
        await ctx.send("✅ Bağlantı tazelendi!")
    else:
        await ctx.send("❌ Yine başarısız... Session ID'yi kontrol edin.")

if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ HATA: DISCORD_TOKEN bulunamadı!")
