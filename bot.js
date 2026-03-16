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
    console.log(`Bot hazır! Giriş: ${client.user.tag}`);
});

// Komutları dinleme
client.on('messageCreate', async message => {
    if (message.author.bot) return;

    // Sunucu aç
    if (message.content === '!sunucuac') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/start`,
                {},
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('Sunucu başlatılıyor! ⏳');
        } catch (err) {
            console.error(err);
            message.reply('Sunucu açılamadı! ❌');
        }
    }

    // Sunucu kapat
    if (message.content === '!sunucukapat') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/stop`,
                {},
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('Sunucu kapatılıyor! ⏳');
        } catch (err) {
            console.error(err);
            message.reply('Sunucu kapatılamadı! ❌');
        }
    }
});

// Bot giriş
client.login(DISCORD_TOKEN);
