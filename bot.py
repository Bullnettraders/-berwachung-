import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Eingelesene Kanal-IDs aus Umgebungsvariablen
WATCH_CHANNEL_IDS = [int(id.strip()) for id in os.getenv("WATCH_CHANNEL_IDS").split(",")]
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id not in WATCH_CHANNEL_IDS:
        return

    # Prüfen: Enthält Nachricht einen GIF-Anhang?
    has_gif_attachment = any(
        (attachment.content_type or "").startswith("image/gif")
        for attachment in message.attachments
    )

    # Prüfen: Enthält Nachricht einen Tenor- oder Giphy-Link?
    has_gif_link = any(domain in message.content.lower() for domain in ["tenor.com", "giphy.com"])

    if has_gif_attachment or has_gif_link:
        await message.delete()
        alert_channel = bot.get_channel(ALERT_CHANNEL_ID)
        if alert_channel:
            await alert_channel.send(
                f"🚨 GIF gelöscht von {message.author.mention} in <#{message.channel.id}>"
            )

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
