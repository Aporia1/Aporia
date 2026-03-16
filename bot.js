const { Client, GatewayIntentBits } = require('discord.js');
const axios = require('axios');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const EXAROTON_API_KEY = process.env.EXAROTON_API_KEY;
const SERVER_ID = process.env.SERVER_ID;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.once('ready', () => {
    console.log(`Bot hazır! Giriş: ${client.user.tag}`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;

    const sendError = (err) => {
        console.error(err.response ? err.response.data : err.message);
        message.reply('Sunucu açılamadı! ❌');
    };

    if (message.content === '!sunucuac') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/start`,
                null,
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('Sunucu başlatılıyor! ⏳');
        } catch (err) {
            sendError(err);
        }
    }

    if (message.content === '!sunucukapat') {
        try {
            await axios.post(
                `https://api.exaroton.com/v1/servers/${SERVER_ID}/stop`,
                null,
                { headers: { Authorization: `Bearer ${EXAROTON_API_KEY}` } }
            );
            message.reply('Sunucu kapatılıyor! ⏳');
        } catch (err) {
            sendError(err);
        }
    }
});

client.login(DISCORD_TOKEN);
