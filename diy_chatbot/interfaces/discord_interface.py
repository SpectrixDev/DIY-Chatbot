import discord
import asyncio
from discord.ext import commands
from diy_chatbot.core.chatbot_engine import Chatbot
from pathlib import Path
import os

def run_discord(
    db_path: str = None,
    discord_token: str = None,
    chatbot_channel_id: int = None
):
    """
    Run the chatbot as a Discord bot.
    """
    if db_path is None:
        db_path = str(Path(__file__).resolve().parent.parent.parent / "data" / "botBrain.sqlite")
    chatbot = Chatbot(db_path)

    # Load token and channel ID from environment if not provided
    if discord_token is None:
        discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    if chatbot_channel_id is None:
        try:
            chatbot_channel_id = int(os.environ.get("CHATBOT_CHANNEL_ID"))
        except (TypeError, ValueError):
            chatbot_channel_id = None

    if not discord_token or not chatbot_channel_id:
        print("Error: Discord bot token or channel ID not provided.")
        return

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(name="your messages and learning...", type=3))
        print("=========\nConnected to Discord\n=========")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.channel.id != chatbot_channel_id:
            return

        # Get last bot message in channel, or use default
        async for msg in message.channel.history(limit=10):
            if msg.author == bot.user:
                bot_message = msg.content
                break
        else:
            bot_message = "Hello, world."

        user_input = message.content.strip()
        chatbot.learn(bot_message, user_input)
        bot_response = chatbot.get_response(user_input)
        await message.channel.send(bot_response)

    try:
        bot.run(discord_token)
    finally:
        chatbot.close()
