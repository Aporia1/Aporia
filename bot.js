const { Client, GatewayIntentBits } = require('discord.js');
const axios = require('axios');

// Environment Variables
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const EXAROTON_API_KEY = process.env.EXAROTON_API_KEY;
const SERVER_ID = process.env.SERVER_ID;

// Discord Client
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Bot hazır olduğunda
client.once('ready', () => {
    console.log(`✅ Bot hazır! Giriş: ${client.user.tag}`);
});

// Hata loglama fonksiyonu
const logError = (message, err) => {
    console.error("Hata detayları:", err.response ? err.response.data : err.message);
    message.reply('❌ İşlem başarısız oldu. Hata logları konsolda.');
};

// Komutları dinleme
client.on('messageCreate', async message => {
    if (message.author.bot) return;

    // !sunucuac komutu
    if (message.content === '!sunucuac') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/start`,
                null,
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('⏳ Sunucu başlatılıyor...');
        } catch (err) {
            logError(message, err);
        }
    }

    // !sunucukapat komutu
    if (message.content === '!sunucukapat') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/stop`,
                null,
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('⏳ Sunucu kapatılıyor...');
        } catch (err) {
            logError(message, err);
        }
    }
});

// Bot giriş
client.login(DISCORD_TOKEN);
