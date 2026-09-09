# Dual-Engine Discord AI Agent (Grok & Claude)

A fully featured, modular Discord bot built in Python (`discord.py`) that supports **intelligent text chat** and **voice channel interactions (Text-to-Speech)**. It supports switching between **xAI Grok** and **Anthropic Claude** on the fly.

## Features

- **Dual AI Support:** Seamlessly switch between Grok and Claude.
- **Text Chat (`!chat`):** Maintains conversational context per user.
- **Voice Channel TTS (`!speak` / `!join` / `!leave`):** Automatically joins your voice channel, converts AI responses into natural speech using Edge-TTS, and speaks them out loud.
- **Provider Switching (`!provider`):** Switch between Grok and Claude instantly in chat.
- **History Management (`!clear`):** Reset your conversational context anytime.

---

## Prerequisites & Installation

### 1. Install Dependencies
Make sure you have Python 3.10+ and `ffmpeg` installed on your system. Then install the required Python packages:

```bash
pip install "discord.py[voice]" openai anthropic python-dotenv edge-tts PyNaCl
```

### 2. Configuration (`.env`)
Copy `.env.template` to `.env` and fill in your credentials:

```bash
cp .env.template .env
```

Open `.env` and add:
- Your **Discord Bot Token**
- Your **xAI API Key** (for Grok) and/or **Anthropic API Key** (for Claude)

---

## How to Get Your Tokens

### Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and give it a name.
3. Navigate to the **Bot** tab on the left menu and click **Reset Token** (or Copy Token).
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
5. Go to **OAuth2 > URL Generator**, select `bot`, and choose permissions: `Send Messages`, `Connect`, `Speak`, `Read Message History`.
6. Copy the generated URL and open it in your browser to invite the bot to your server.

### AI API Keys
- **Grok (xAI):** Get your key from the [xAI Console](https://console.x.ai/).
- **Claude (Anthropic):** Get your key from the [Anthropic Console](https://console.anthropic.com/).

---

## Running the Bot

Run the bot script from your terminal:

```bash
python bot.py
```

---

## Bot Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `!chat <message>` | Send a prompt to the active AI and get a text response. | `!chat What is the speed of light?` |
| `!provider <grok/claude>` | Switch your AI backend between Grok and Claude. | `!provider claude` |
| `!join` | Have the bot join your current voice channel. | `!join` |
| `!leave` | Have the bot leave the voice channel. | `!leave` |
| `!speak <message>` | Send a prompt, get a response, and hear it spoken in voice. | `!speak Tell me a joke` |
| `!clear` | Clear your active conversation history. | `!clear` |
