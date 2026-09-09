import os
import asyncio
import discord
from discord.ext import commands
from openai import OpenAI
from anthropic import Anthropic
import edge_tts

# --- CONFIGURATION ---
# These will be pulled from Replit Secrets
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_PROVIDER = os.getenv("AI_PROVIDER", "grok").lower()

# --- AI CLIENTS ---
class GrokClient:
    def __init__(self):
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-2"
        self.client = OpenAI(api_key=XAI_API_KEY, base_url=self.base_url) if XAI_API_KEY else None

    def get_response(self, history):
        if not self.client: return "Error: xAI API Key missing."
        models = [self.model, "grok-2", "grok-beta", "grok-latest"]
        last_err = ""
        for m in list(dict.fromkeys(models)):
            try:
                resp = self.client.chat.completions.create(model=m, messages=history)
                self.model = m
                return resp.choices[0].message.content
            except Exception as e:
                last_err = str(e)
                if "Model not found" in last_err or "invalid-argument" in last_err: continue
                else: break
        return f"Grok Error: {last_err}"

class ClaudeClient:
    def __init__(self):
        self.model = "claude-3-5-sonnet-20241022"
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

    def get_response(self, history):
        if not self.client: return "Error: Claude API Key missing."
        try:
            sys = next((m["content"] for m in history if m["role"] == "system"), "You are a helpful assistant.")
            msgs = [m for m in history if m["role"] != "system"]
            resp = self.client.messages.create(model=self.model, max_tokens=1024, system=sys, messages=msgs)
            return resp.content[0].text
        except Exception as e: return f"Claude Error: {e}"

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

grok = GrokClient()
claude = ClaudeClient()
chat_history = {}
user_provider = {}

def get_client(uid):
    prov = user_provider.get(uid, DEFAULT_PROVIDER)
    return (claude, "Claude") if prov == "claude" else (grok, "Grok")

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")

@bot.command()
async def provider(ctx, p: str):
    p = p.lower()
    if p in ["grok", "claude"]:
        user_provider[ctx.author.id] = p
        await ctx.send(f"Switched to **{p.upper()}**")
    else:
        await ctx.send("Use `!provider grok` or `!provider claude`")

@bot.command()
async def chat(ctx, *, msg: str):
    uid = ctx.author.id
    client, name = get_client(uid)
    if uid not in chat_history: chat_history[uid] = [{"role": "system", "content": "Helpful Discord AI."}]
    chat_history[uid].append({"role": "user", "content": msg})
    
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, client.get_response, chat_history[uid])
    
    chat_history[uid].append({"role": "assistant", "content": resp})
    await ctx.send(f"**[{name}]** {resp[:1900]}")

@bot.command()
async def speak(ctx, *, msg: str):
    if not ctx.author.voice: return await ctx.send("Join a voice channel first!")
    
    vc = ctx.voice_client
    if not vc: vc = await ctx.author.voice.channel.connect()
    elif vc.channel != ctx.author.voice.channel: await vc.move_to(ctx.author.voice.channel)
    
    uid = ctx.author.id
    client, name = get_client(uid)
    if uid not in chat_history: chat_history[uid] = [{"role": "system", "content": "Helpful Discord AI. Keep it short."}]
    chat_history[uid].append({"role": "user", "content": msg})
    
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, client.get_response, chat_history[uid])
    
    chat_history[uid].append({"role": "assistant", "content": resp})
    await ctx.send(f"**{name} says:** {resp[:1900]}")
    
    # TTS
    tts_file = "voice.mp3"
    await edge_tts.Communicate(resp, "en-US-AndrewNeural").save(tts_file)
    if vc.is_playing(): vc.stop()
    vc.play(discord.FFmpegPCMAudio(tts_file))

@bot.command()
async def leave(ctx):
    if ctx.voice_client: await ctx.voice_client.disconnect()

if __name__ == "__main__":
    if not TOKEN: print("Missing DISCORD_BOT_TOKEN in Secrets!")
    else: bot.run(TOKEN)
