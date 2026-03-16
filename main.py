import discord
from discord.ext import commands
import aiohttp
from aiohttp import web
import os
import asyncio

# Güvenlik için token ve anahtarları ortam değişkenlerinden (Railway üzerinden) alıyoruz
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
EXAROTON_API_KEY = os.environ.get("EXAROTON_API_KEY")
SERVER_ID = os.environ.get("SERVER_ID")

# Botun mesajları okuyabilmesi için gerekli izinleri (Intents) açıyoruz
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 1. BÖLÜM: SAHTE WEB SUNUCUSU (RAILWAY'İ KANDIRMAK İÇİN) ---
async def handle(request):
    # Railway sağlığımızı kontrol ettiğinde bu mesajı döneceğiz
    return web.Response(text="Minecraft Sunucu Botu Aktif ve Calisiyor!")

async def web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Railway'in bize atadığı portu alıyoruz, bulamazsa 8080 kullanıyoruz
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web sunucusu {port} portunda başlatıldı. Railway artık çökmediğimizi biliyor.")

# --- 2. BÖLÜM: DİSCORD BOTU KODLARI ---
@bot.event
async def on_ready():
    print(f'✅ {bot.user} olarak giriş yapıldı ve bot çevrimiçi!')

@bot.command(name="sunucuac", help="Exaroton Minecraft sunucusunu başlatır.")
async def sunucuac(ctx):
    if not EXAROTON_API_KEY or not SERVER_ID:
        await ctx.send("❌ API Anahtarı veya Sunucu ID eksik! Lütfen Railway ayarlarını kontrol edin.")
        return

    await ctx.send("⏳ Sunucuya başlatma sinyali gönderiliyor, lütfen bekleyin...")

    url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/start"
    headers = {"Authorization": f"Bearer {EXAROTON_API_KEY}"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers) as response:
                if response.status == 200:
                    await ctx.send("🟢 Başarılı! Sunucu açılıyor. Birkaç dakika içinde oyuna katılabilirsiniz.")
                elif response.status == 400:
                    await ctx.send("⚠️ Sunucu şu anda başlatılamıyor. Zaten açık veya açılış aşamasında olabilir.")
                elif response.status == 401:
                    await ctx.send("❌ Exaroton API Anahtarı geçersiz veya yetkisiz!")
                elif response.status == 404:
                    await ctx.send("❌ Sunucu bulunamadı! SERVER_ID değerini kontrol edin.")
                else:
                    await ctx.send(f"❌ Beklenmeyen bir durum oluştu. HTTP Kodu: {response.status}")
        except Exception as e:
            await ctx.send(f"❌ API'ye bağlanırken bir hata oluştu: {str(e)}")

# --- 3. BÖLÜM: HER İKİSİNİ AYNI ANDA ÇALIŞTIRMA ---
async def main():
    # Hem sahte web sunucusunu hem de Discord botunu aynı anda başlatıyoruz
    await asyncio.gather(
        web_server(),
        bot.start(DISCORD_TOKEN)
    )

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("HATA: DISCORD_TOKEN bulunamadı! Lütfen Railway ortam değişkenlerine ekleyin.")
    else:
        # Asenkron döngüyü başlatıyoruz
        asyncio.run(main())
