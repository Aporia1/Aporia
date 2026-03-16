const { Client, GatewayIntentBits } = require('discord.js');
const axios = require('axios');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const EXAROTON_API_KEY = process.env.EXAROTON_API_KEY;
const SERVER_ID = process.env.SERVER_ID;

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', () => {
    console.log(`Bot hazır! Giriş: ${client.user.tag}`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;

    if (message.content === '!sunucuac') {
        try {
            const response = await axios.post(
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

    if (message.content === '!sunucukapat') {
        try {
            const response = await axios.post(
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

client.login(DISCORD_TOKEN);
