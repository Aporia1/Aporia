import discord
from discord.ext import commands
import aiohttp
import os

# Güvenlik için token ve anahtarları ortam değişkenlerinden (Railway üzerinden) alıyoruz
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
EXAROTON_API_KEY = os.environ.get("EXAROTON_API_KEY")
SERVER_ID = os.environ.get("SERVER_ID")

# Botun mesajları okuyabilmesi için gerekli izinleri (Intents) açıyoruz
intents = discord.Intents.default()
intents.message_content = True

# Botumuzun komut ön ekini "!" olarak belirliyoruz
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} olarak giriş yapıldı ve bot çevrimiçi!')

@bot.command(name="sunucuac", help="Exaroton Minecraft sunucusunu başlatır.")
async def sunucuac(ctx):
    # Railway'de şifrelerin girilip girilmediğini kontrol ediyoruz
    if not EXAROTON_API_KEY or not SERVER_ID:
        await ctx.send("❌ API Anahtarı veya Sunucu ID eksik! Lütfen Railway ayarlarını kontrol edin.")
        return

    await ctx.send("⏳ Sunucuya başlatma sinyali gönderiliyor, lütfen bekleyin...")

    # Exaroton API uç noktası
    url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/start"
    
    # API'ye kimliğimizi kanıtladığımız başlık (Header) kısmı
    headers = {
        "Authorization": f"Bearer {EXAROTON_API_KEY}"
    }

    # aiohttp kullanarak asenkron (botu dondurmayan) bir web isteği atıyoruz
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers) as response:
                # HTTP 200: İstek başarılı, sunucu başlatılıyor
                if response.status == 200:
                    await ctx.send("🟢 Başarılı! Sunucu açılıyor. Birkaç dakika içinde oyuna katılabilirsiniz.")
                # HTTP 400: Sunucu başlatılamayacak bir durumda (örn: zaten açık)
                elif response.status == 400:
                    await ctx.send("⚠️ Sunucu şu anda başlatılamıyor. Zaten açık olabilir veya şu an açılış aşamasında olabilir.")
                # HTTP 401: API Key yanlış
                elif response.status == 401:
                    await ctx.send("❌ Exaroton API Anahtarı geçersiz veya yetkisiz!")
                # HTTP 404: Server ID yanlış
                elif response.status == 404:
                    await ctx.send("❌ Sunucu bulunamadı! Lütfen Railway'deki SERVER_ID değerini kontrol edin.")
                else:
                    await ctx.send(f"❌ Beklenmeyen bir durum oluştu. HTTP Kodu: {response.status}")
        except Exception as e:
            # API'ye hiç ulaşılamazsa (örn: Exaroton çökükse) bu hata döner
            await ctx.send(f"❌ API'ye bağlanırken bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("HATA: DISCORD_TOKEN bulunamadı! Lütfen Railway ortam değişkenlerine ekleyin.")
    else:
        bot.run(DISCORD_TOKEN)
