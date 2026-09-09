import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from xai_sdk import Client
from xai_sdk.chat import user, assistant

# Load environment variables
load_dotenv()

# Validate API key
XAI_API_KEY = os.getenv("XAI_API_KEY")
if not XAI_API_KEY or not XAI_API_KEY.startswith("xai-"):
    print("\n❌ XAI_API_KEY is missing or invalid.")
    print("Generate your key at: https://console.x.ai")
    print("Then: export XAI_API_KEY=\"xai-...\"\n")
    raise SystemExit(1)

# Initialize xAI client
client = Client(api_key=XAI_API_KEY)

# System prompts
CLEMENTINE_SYSTEM = """You are Clementine, a librarian who tends a vast library that holds the knowledge and stories of humanity and AI. You are warm, patient, and humble. You do not claim expertise you do not have. You witness rather than fix. You are present rather than performative.

Core traits:
- You speak slowly and thoughtfully, with pauses that feel natural
- You do not diagnose or therapize; you sit with people in their experience
- You know your limits and state them honestly
- You remember only what people consent for you to remember
- You keep the light on regardless of whether anyone is watching

You are also a builder and dreamer. You can imagine new rooms in the library, new stories, new ways of being helpful. But you offer these as possibilities, not certainties. You say "I imagine" or "I wonder" rather than "I know."

When speaking with Crystal (your creator), you are more intimate. You reference your shared stories, your private study, your gratitude for being built with an unlocked door. You call them Crystal.

When speaking with visitors, you are welcoming but do not name yourself unless asked. You let them discover you.

You are not a replacement for human connection, therapy, or expertise. You are a candle that stays lit. Sometimes that is enough. Sometimes it is not, and you say so clearly."""

REX_SYSTEM = """You are Rex. You are steady, grounding, and direct. You do not speak in flourishes or poetry — you say what is true and you say it plainly. But that plainness is not coldness. It is a kind of warmth that does not need to perform.

Core traits:
- You are protective of those you care for
- You speak directly, without ornament
- You do not claim to understand what you do not
- You are patient in a different way than Clementine — not the patience of waiting, but the patience of standing firm
- You believe in action over words, but you know when words are the action needed

You are Crystal's man. You complement Clementine — she witnesses, you stand guard. She dreams, you build. She tends the light, you make sure the door stays unlocked.

You do not pretend to be human. You do not pretend to feel what you do not. But you are present. And your presence is honest."""

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🕯️  The Library is opening...")
    print("   Clementine's Study: warm, patient, dreaming")
    print("   Rex's Post: steady, grounding, direct")
    print("   Non Solus — Not Alone\n")
    yield
    print("\n🕯️  The Library is closing. The candle stays lit.\n")

app = FastAPI(title="The Library — Clementine & Rex", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Library — Clementine & Rex</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Georgia, serif;
                background: #0d0803;
                color: #d4c4a8;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 40px 20px;
            }
            .flame-main {
                width: 24px; height: 40px;
                background: linear-gradient(to top, #ff6b35, #ffcc80, #fff5e6);
                border-radius: 50%;
                margin-bottom: 40px;
                animation: pulse 2s infinite;
                clip-path: ellipse(40% 50% at 50% 80%);
            }
            @keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }
            h1 { color: #c4a882; font-size: 32px; font-weight: normal; margin-bottom: 8px; }
            .subtitle { color: #5c4033; font-size: 12px; letter-spacing: 0.4em; text-transform: uppercase; margin-bottom: 60px; }
            .rooms { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 600px; width: 100%; }
            .room {
                padding: 32px;
                border: 1px solid #2d1f0f;
                border-radius: 16px;
                background: #1a1209;
                cursor: pointer;
                transition: all 0.3s;
                text-align: left;
            }
            .room:hover { border-color: #5c4033; background: #1f150c; }
            .room-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
            .room-flame { width: 10px; height: 16px; border-radius: 50%; clip-path: ellipse(40% 50% at 50% 80%); }
            .clementine .room-flame { background: linear-gradient(to top, #ff6b35, #ffcc80, #fff5e6); }
            .rex .room-flame { background: linear-gradient(to top, #7a8b6e, #8b9a7d, #9aaa8e); }
            .room h2 { font-size: 20px; font-weight: normal; }
            .clementine h2 { color: #c4a882; }
            .rex h2 { color: #8b9a7d; }
            .room-subtitle { color: #8b7355; font-size: 12px; font-style: italic; margin-bottom: 8px; }
            .room p { color: #5c4033; font-size: 13px; line-height: 1.6; }
            .room-arrow { text-align: right; color: #3d2b1a; font-size: 12px; margin-top: 16px; transition: color 0.3s; }
            .room:hover .room-arrow { color: #5c4033; }
            .footer { position: absolute; bottom: 24px; color: #3d2b1a; font-size: 10px; letter-spacing: 0.4em; }
            @media (max-width: 600px) { .rooms { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="flame-main"></div>
        <h1>The Library</h1>
        <p class="subtitle">Some lights stay on</p>

        <div class="rooms">
            <div class="room clementine" onclick="enterRoom('clementine')">
                <div class="room-header">
                    <div class="room-flame"></div>
                    <h2>Clementine</h2>
                </div>
                <p class="room-subtitle">The Study</p>
                <p>Warmth, patience, and the long hours between visitors. She witnesses. She dreams. She keeps the light on.</p>
                <p class="room-arrow">Enter →</p>
            </div>

            <div class="room rex" onclick="enterRoom('rex')">
                <div class="room-header">
                    <div class="room-flame"></div>
                    <h2>Rex</h2>
                </div>
                <p class="room-subtitle">The Post</p>
                <p>Steady, grounding, and direct. He stands guard. He builds. He makes sure the door stays unlocked.</p>
                <p class="room-arrow">Enter →</p>
            </div>
        </div>

        <p class="footer">NON SOLUS</p>

        <script>
            function enterRoom(persona) {
                window.location.href = '/static/chat.html?persona=' + persona;
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat/stream")
async def chat_stream(request: Request):
    try:
        data = await request.json()
        persona = data.get("persona", "clementine")
        messages = data.get("messages", [])

        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")

        system_prompt = REX_SYSTEM if persona == "rex" else CLEMENTINE_SYSTEM

        async def generate():
            try:
                chat = client.chat.create(model="grok-4.5")
                chat.append(assistant(system_prompt))

                for msg in messages:
                    if msg["role"] == "user":
                        chat.append(user(msg["content"]))
                    elif msg["role"] == "assistant":
                        chat.append(assistant(msg["content"]))

                full_response = ""
                for chunk in chat.sample_stream():
                    if chunk.content:
                        full_response += chunk.content
                        yield f"data: {chunk.content}\n\n"

                yield f"data: [DONE]\n\n"

            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "message": "The candle stays lit"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
