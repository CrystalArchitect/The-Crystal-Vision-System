import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from grok_client import GrokClient
from claude_client import ClaudeClient
from voice_manager import VoiceManager

load_dotenv()

# Discord Bot Setup
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEFAULT_PROVIDER = os.getenv("AI_PROVIDER", "grok").lower() # 'grok' or 'claude'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Clients
grok = GrokClient()
claude = ClaudeClient()
voice = VoiceManager()

# Per-user settings and chat history
chat_history = {}
user_provider = {} # Allows users to switch between grok and claude per session/user

def get_active_client(user_id):
    provider = user_provider.get(user_id, DEFAULT_PROVIDER)
    if provider == "claude":
        return claude, "Claude"
    else:
        return grok, "Grok"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Default AI Provider: {DEFAULT_PROVIDER.upper()}")
    print("------")

@bot.command(name="provider")
async def set_provider(ctx, provider: str):
    """Switch your AI provider between 'grok' and 'claude'."""
    provider = provider.lower()
    if provider in ["grok", "claude"]:
        user_provider[ctx.author.id] = provider
        await ctx.send(f"AI provider switched to **{provider.upper()}** for you!")
    else:
        await ctx.send("Invalid provider. Choose either `grok` or `claude`.")

@bot.command(name="chat")
async def chat(ctx, *, message: str):
    """Sends a message to the active AI (Grok or Claude) and gets a text response."""
    user_id = ctx.author.id
    client, provider_name = get_active_client(user_id)
    
    if user_id not in chat_history:
        chat_history[user_id] = []
    
    chat_history[user_id].append({"role": "user", "content": message})
    
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, client.get_response, chat_history[user_id])
        
    chat_history[user_id].append({"role": "assistant", "content": response})
    
    # Format response with provider tag
    prefix = f"**[{provider_name}]** "
    full_response = prefix + response
    
    if len(full_response) > 2000:
        await ctx.send(prefix)
        for i in range(0, len(response), 2000):
            await ctx.send(response[i:i+2000])
    else:
        await ctx.send(full_response)

@bot.command(name="join")
async def join(ctx):
    """Joins the user's voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await voice.join_channel(channel)
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command(name="leave")
async def leave(ctx):
    """Leaves the voice channel."""
    await voice.leave_channel()
    await ctx.send("Left the voice channel.")

@bot.command(name="speak")
async def speak(ctx, *, message: str):
    """Sends a message to the active AI and speaks the response in the voice channel."""
    if not voice.voice_client:
        await ctx.invoke(join)
    
    user_id = ctx.author.id
    client, provider_name = get_active_client(user_id)
    
    if user_id not in chat_history:
        chat_history[user_id] = []
    
    chat_history[user_id].append({"role": "user", "content": message})
    
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, client.get_response, chat_history[user_id])
        
    chat_history[user_id].append({"role": "assistant", "content": response})
    
    await ctx.send(f"**{provider_name} says:** {response}")
    await voice.speak(response)

@bot.command(name="clear")
async def clear(ctx):
    """Clears your conversation history."""
    user_id = ctx.author.id
    if user_id in chat_history:
        chat_history[user_id] = []
    await ctx.send("Your conversation history has been cleared.")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables.")
    else:
        bot.run(TOKEN)
