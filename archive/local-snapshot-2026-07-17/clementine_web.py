"""
Clementine — local web interface

Runs only on your own machine (bound to 127.0.0.1, never exposed).
Shares the same brain and memory folder as the terminal version, so you
can switch between them freely. Nothing leaves your device.

    pip install -r requirements.txt
    python clementine_web.py            # then open http://127.0.0.1:5000
"""

import argparse
from pathlib import Path

from flask import (Flask, Response, abort, jsonify, render_template_string,
                   request)

from crystalcore import (Clementine, delete_profile, full_expose, list_profiles,
                         profile_dir, profile_meta)
from crystalcore import profiles as _profiles
from crystalcore.expose import companion_dump

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ name }} — sovereign companion</title>
<style>
  :root{--bg:#000004;--ink:#E9EBF4;--muted:#A6ACC4;--purple:#A78BFA;
        --card:#07070F;--line:rgba(233,235,244,.12)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font-family:system-ui,sans-serif;
       display:flex;flex-direction:column;height:100vh}
  header{padding:14px 20px;border-bottom:1px solid var(--line);
         display:flex;justify-content:space-between;align-items:center}
  header b{color:var(--purple)}
  header small{color:var(--muted)}
  main{flex:1;display:flex;min-height:0}
  #chatcol{flex:2;display:flex;flex-direction:column;min-width:0}
  #log{flex:1;overflow-y:auto;padding:20px}
  .msg{max-width:70ch;margin:0 0 14px;padding:10px 14px;border-radius:12px;
       white-space:pre-wrap;line-height:1.55}
  .you{background:#141420;margin-left:auto}
  .her{background:var(--card);border:1px solid var(--line)}
  .her b{color:var(--purple)}
  form#send{display:flex;gap:10px;align-items:flex-end;padding:14px 20px;border-top:1px solid var(--line)}
  input,button,textarea{font:inherit;color:var(--ink);background:#0D0D18;
       border:1px solid var(--line);border-radius:8px;padding:10px}
  input{flex:1}
  textarea#box{flex:1;resize:none;line-height:1.4;max-height:160px}
  button{cursor:pointer;background:var(--purple);color:#050208;border:none;
         font-weight:600;padding:10px 18px}
  button.small{padding:2px 9px;font-weight:400;background:transparent;
               color:var(--muted);border:1px solid var(--line)}
  aside{flex:1;max-width:340px;border-left:1px solid var(--line);
        padding:16px;overflow-y:auto}
  aside h2{font-size:.95rem;color:var(--muted);margin-bottom:10px;
           text-transform:uppercase;letter-spacing:.08em}
  .mem{display:flex;justify-content:space-between;gap:8px;align-items:start;
       padding:8px 0;border-bottom:1px solid var(--line);font-size:.92rem}
  .mem .tags{color:var(--purple);font-size:.8rem}
  #teach{display:flex;flex-direction:column;gap:8px;margin-top:14px}
  footer{padding:10px 20px;color:var(--muted);font-size:.8rem;
         border-top:1px solid var(--line)}
  @media(max-width:760px){aside{display:none}}
</style>
</head>
<body>
<header><div><span id="heravatar"></span> <b id="hername">{{ name }}</b> · sovereign companion</div>
<div style="display:flex;gap:8px;align-items:center">
  <button class="small" id="voicebtn" type="button" aria-pressed="false"
    title="Speak her replies aloud (on-device voice)">🔇 voice</button>
  <select id="voicepick" title="Which voice she speaks with" style="max-width:150px"></select>
  <select id="profiles" title="Profile — separate person, separate memory"></select>
  <input id="newprofile" placeholder="new profile" size="9">
  <button class="small" id="mkprofile" type="button">create</button>
  <small id="bindhint">UI · 127.0.0.1</small>
</div></header>
<main>
  <div id="chatcol">
    <div id="log"></div>
    <form id="send">
      <textarea id="box" rows="1" autocomplete="off" autofocus
        placeholder="Say something… (Enter to send, Shift+Enter for a new line)"></textarea>
      <button type="button" id="mic" class="small" title="Hold a conversation: click and speak">🎤 talk</button>
      <button>Send</button>
      <button type="button" id="stop" class="small" style="display:none">Stop</button>
    </form>
  </div>
  <aside>
    <h2>Her memory <button class="small" id="reflectbtn" type="button"
        title="Invite her to form gentle insights about you">reflect</button></h2>
    <div id="mems"></div>
    <form id="teach">
      <input id="teachtext" placeholder="Teach her something… (#tags ok)">
      <input id="teachkey" placeholder="Optional fact key (e.g. birthday)">
      <button>Remember</button>
    </form>
    <h2 style="margin-top:22px">This profile</h2>
    <form id="pmeta">
      <input id="pavatar" placeholder="Avatar emoji, e.g. 🌟" size="12">
      <input id="pdesc" placeholder="Short description" style="width:100%;margin-top:8px">
      <input id="pmodel" placeholder="Model (llama3.1:8b or grok-4.5)" style="width:100%;margin-top:8px">
      <label style="display:block;margin-top:8px;color:var(--muted);font-size:.85rem">Chat provider
        <select id="pprovider" style="width:100%;margin-top:4px">
          <option value="ollama">ollama (local)</option>
          <option value="spacexai">spacexai (opt-in · xAI API)</option>
        </select>
      </label>
      <p id="optinhint" style="margin:6px 0 0;font-size:.8rem;color:var(--muted)">
        SpaceXAI requires explicit opt-in: chat leaves this device; memory stays local.
      </p>
      <button style="margin-top:8px">Save profile</button>
    </form>
    <div style="margin-top:14px">
      <button class="small" id="delprofile" type="button">delete another profile…</button>
    </div>
  </aside>
</main>
<footer id="foot">Memory is always local. Chat uses the selected provider.
Non solus.</footer>
<script>
const log = document.getElementById('log');
function bubble(who, text){
  const d = document.createElement('div');
  d.className = 'msg ' + (who === 'you' ? 'you' : 'her');
  d.textContent = text;                 // textContent: nothing is ever HTML
  log.appendChild(d); log.scrollTop = log.scrollHeight;
  return d;
}

// ---- her voice: on-device speech synthesis (no install, nothing leaves) ----
const synth = window.speechSynthesis;
let voiceOn = localStorage.getItem('voiceOn') === '1';
let voices = [];
const voiceBtn = document.getElementById('voicebtn');
const voicePick = document.getElementById('voicepick');
function paintVoiceBtn(){
  voiceBtn.textContent = (voiceOn ? '🔊' : '🔇') + ' voice';
  voiceBtn.setAttribute('aria-pressed', voiceOn ? 'true' : 'false');
}
function loadVoices(){
  if (!synth) return;
  voices = synth.getVoices();
  const saved = localStorage.getItem('voiceName') || '';
  voicePick.innerHTML = '';
  voices.forEach((v, i) => {
    const o = document.createElement('option');
    o.value = v.name;
    o.textContent = v.name + (v.lang ? ' (' + v.lang + ')' : '');
    if (v.name === saved) o.selected = true;
    voicePick.appendChild(o);
  });
}
function chosenVoice(){
  const name = voicePick.value || localStorage.getItem('voiceName');
  return voices.find(v => v.name === name) || null;
}
function speak(text, onDone){
  if (!voiceOn || !synth || !text.trim()){ if (onDone) onDone(); return; }
  synth.cancel();                       // never let two replies overlap
  const u = new SpeechSynthesisUtterance(text);
  const v = chosenVoice();
  if (v){ u.voice = v; u.lang = v.lang; }
  u.rate = 1.0; u.pitch = 1.0;
  u.onend = () => { if (onDone) onDone(); };
  u.onerror = () => { if (onDone) onDone(); };
  synth.speak(u);
}
function stopSpeaking(){ if (synth) synth.cancel(); }
if (synth){
  paintVoiceBtn();
  loadVoices();
  synth.onvoiceschanged = loadVoices;   // voices load async in most browsers
  voiceBtn.onclick = () => {
    voiceOn = !voiceOn;
    localStorage.setItem('voiceOn', voiceOn ? '1' : '0');
    if (!voiceOn) stopSpeaking();
    paintVoiceBtn();
  };
  voicePick.onchange = () => localStorage.setItem('voiceName', voicePick.value);
} else {
  voiceBtn.style.display = 'none';
  voicePick.style.display = 'none';
}

// ---- her ears: a hands-free back-and-forth conversation ----
// One click starts conversation mode: she listens, you speak, she replies
// aloud, then she listens again on her own — until you click to end it.
const micBtn = document.getElementById('mic');
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recog = null, listening = false, convoMode = false;
function paintMic(){
  if (!convoMode){ micBtn.textContent = '🎤 talk'; micBtn.style.color = ''; return; }
  micBtn.textContent = listening ? '🔴 listening… (click to end)'
                                 : '🟣 in conversation (click to end)';
  micBtn.style.color = listening ? '#F87171' : '#A78BFA';
}
function startListening(){
  if (!recog || listening) return;
  stopSpeaking();                      // don't let her voice feed back into the mic
  try { recog.start(); } catch (_) {}
}
// Called after she finishes replying (and speaking); pick up the next turn.
function resumeConversation(){ if (convoMode) startListening(); }
if (SR){
  recog = new SR();
  recog.lang = 'en-US';
  recog.interimResults = true;         // show words as you speak
  recog.continuous = false;            // one turn, then send
  let finalText = '';
  recog.onstart = () => { listening = true; finalText = ''; paintMic(); };
  recog.onerror = () => { listening = false; paintMic(); };
  recog.onend = () => {
    listening = false; paintMic();
    const said = (finalText || '').trim();
    if (said){ boxEl.value = said; document.getElementById('send').requestSubmit(); }
    else if (convoMode){ startListening(); }   // stayed silent — keep listening
  };
  recog.onresult = (e) => {
    let interim = '';
    for (let i = e.resultIndex; i < e.results.length; i++){
      const chunk = e.results[i][0].transcript;
      if (e.results[i].isFinal) finalText += chunk; else interim += chunk;
    }
    boxEl.value = (finalText + interim).trim();   // live preview in the box
  };
  micBtn.onclick = () => {
    convoMode = !convoMode;
    if (convoMode){
      if (!voiceOn){ voiceOn = true; localStorage.setItem('voiceOn','1'); paintVoiceBtn(); }
      paintMic(); startListening();
    } else {
      if (listening) recog.stop();
      stopSpeaking(); paintMic();
    }
  };
} else {
  micBtn.style.display = 'none';
}
async function refreshMems(){
  const r = await fetch('/api/memories'); const data = await r.json();
  const box = document.getElementById('mems'); box.innerHTML = '';
  const all = [...data.facts, ...data.notes,
               ...(data.reflections || []).map(r => ({...r, text: '✨ ' + r.text}))];
  for (const m of all){
    const row = document.createElement('div'); row.className = 'mem';
    const left = document.createElement('div');
    left.textContent = (m.handle.startsWith('n') && /^n\\d+$/.test(m.handle)
                        ? m.handle + ' · ' : '') + m.text;
    if (m.tags.length){
      const t = document.createElement('div'); t.className = 'tags';
      t.textContent = m.tags.map(x => '#' + x).join(' ');
      left.appendChild(t);
    }
    const btn = document.createElement('button');
    btn.className = 'small'; btn.textContent = 'forget';
    btn.onclick = async () => {
      await fetch('/api/forget', {method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({handle: m.handle})});
      refreshMems();
    };
    row.appendChild(left); row.appendChild(btn); box.appendChild(row);
  }
}
let controller = null;
const stopBtn = document.getElementById('stop');
stopBtn.onclick = () => {
  if (controller) controller.abort();
  stopSpeaking();
  convoMode = false;                    // Stop ends the hands-free conversation
  if (typeof recog !== 'undefined' && recog && listening) recog.stop();
  if (typeof paintMic === 'function') paintMic();
};
const boxEl = document.getElementById('box');
boxEl.oninput = () => {
  boxEl.style.height = 'auto';
  // +2: scrollHeight excludes the 1px top/bottom borders of the border-box
  boxEl.style.height = Math.min(boxEl.scrollHeight + 2, 160) + 'px';
};
boxEl.onkeydown = (e) => {
  if (e.isComposing || e.keyCode === 229) return;  // IME composition: let Enter confirm the candidate
  if (e.key === 'Enter' && !e.shiftKey){
    e.preventDefault();
    document.getElementById('send').requestSubmit();
  }
};
document.getElementById('send').onsubmit = async (e) => {
  e.preventDefault();
  const msg = boxEl.value.trim(); if (!msg) return;
  boxEl.value = ''; boxEl.style.height = 'auto';
  bubble('you', msg);
  const d = bubble('her', '…');
  controller = new AbortController();
  stopBtn.style.display = 'inline-block';
  try {
    const r = await fetch('/api/chat/stream', {method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: msg}), signal: controller.signal});
    if (!r.ok) {
      let detail = '';
      try { detail = (await r.text()).slice(0, 400); } catch (_) {}
      d.textContent = '[error ' + r.status + '] ' +
        (detail || 'Chat request failed. Is Lumina still running on 127.0.0.1?');
      resumeConversation();
    } else if (!r.body) {
      d.textContent = '[error] No response body (try http://127.0.0.1:5000 not another host).';
      resumeConversation();
    } else {
      d.textContent = '';
      const reader = r.body.getReader();
      const dec = new TextDecoder();
      while (true){
        const {done, value} = await reader.read();
        if (done) break;
        d.textContent += dec.decode(value, {stream: true});
        log.scrollTop = log.scrollHeight;
      }
      if (!d.textContent.trim()) {
        d.textContent = '[empty reply] Backend returned nothing. Try again, or switch provider to ollama in the sidebar.';
      }
      speak(d.textContent, resumeConversation);   // say it, then listen again
    }
  } catch (err) {
    if (err && err.name === 'AbortError') {
      d.textContent += d.textContent && d.textContent !== '…' ? ' — [stopped]' : '[stopped]';
    } else {
      const why = (err && err.message) ? err.message : String(err || 'network error');
      d.textContent = '[connection error] ' + why +
        ' — open http://127.0.0.1:5000 (not 0.0.0.0 / not phone on Wi‑Fi).';
    }
    resumeConversation();               // keep the conversation alive on a hiccup
  }
  stopBtn.style.display = 'none';
  controller = null;
  refreshMems();
};
function paintBackend(data){
  const prov = data.provider || 'ollama';
  const model = data.model || '';
  const keyOk = data.xai_key_present;
  const opted = data.cloud_opt_in;
  const foot = document.getElementById('foot');
  const hint = document.getElementById('bindhint');
  const fallback = data.local_fallback;
  const activeProv = data.active_provider || prov;
  const activeModel = data.active_model || model;
  if (prov === 'spacexai' && fallback){
    hint.textContent = 'local fallback · ' + activeModel + ' (no API key)';
    foot.textContent = 'Opted into SpaceXAI but XAI_API_KEY is missing — chatting via local Ollama (' + activeModel + '). Add a key to .env for api.x.ai. Memory stays local. Non solus.';
  } else if (prov === 'spacexai'){
    hint.textContent = 'SpaceXAI · opted in · ' + model + (keyOk ? '' : ' · no key');
    foot.textContent = 'You opted in: chat goes to api.x.ai (' + model + '). Memory files stay on this device. UI is 127.0.0.1 only. Non solus.';
  } else {
    hint.textContent = 'local · 127.0.0.1' + (opted ? ' · cloud opt-in saved but off' : '');
    foot.textContent = 'Local mode. Everything on this page stays on your device unless you opt into SpaceXAI. Non solus.';
  }
  const psel = document.getElementById('pprovider');
  if (psel) psel.value = prov === 'spacexai' ? 'spacexai' : 'ollama';
}
async function refreshProfiles(){
  const r = await fetch('/api/profile'); const data = await r.json();
  const sel = document.getElementById('profiles'); sel.innerHTML = '';
  for (const p of data.profiles){
    const o = document.createElement('option');
    o.value = p.profile;
    o.textContent = (p.avatar ? p.avatar + ' ' : '') + p.profile +
                    (p.description ? ' — ' + p.description : '');
    if (p.profile === data.current){
      o.selected = true;
      document.getElementById('heravatar').textContent = p.avatar || '';
      document.getElementById('pavatar').value = p.avatar || '';
      document.getElementById('pdesc').value = p.description || '';
      document.getElementById('pmodel').value = p.model || '';
      paintBackend({provider: p.provider || data.provider,
                    model: p.model || data.model,
                    xai_key_present: data.xai_key_present});
    }
    sel.appendChild(o);
  }
  if (data.provider) paintBackend(data);
}
async function switchProfile(name){
  const r = await fetch('/api/profile', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({profile: name})});
  const data = await r.json();
  if (data.ok){
    document.getElementById('hername').textContent = data.name;
    log.innerHTML = '';
    bubble('her', `(profile: ${data.profile} — her memory of you here is separate)`);
    if (data.provider || data.model) paintBackend(data);
    refreshProfiles(); refreshMems();
  }
}
document.getElementById('profiles').onchange = (e) => switchProfile(e.target.value);
document.getElementById('mkprofile').onclick = () => {
  const name = document.getElementById('newprofile').value.trim();
  if (name){ document.getElementById('newprofile').value = ''; switchProfile(name); }
};
document.getElementById('teach').onsubmit = async (e) => {
  e.preventDefault();
  const text = document.getElementById('teachtext').value.trim();
  const key = document.getElementById('teachkey').value.trim();
  if (!text) return;
  await fetch('/api/teach', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({text, key})});
  document.getElementById('teachtext').value = '';
  document.getElementById('teachkey').value = '';
  refreshMems();
};
document.getElementById('pmeta').onsubmit = async (e) => {
  e.preventDefault();
  const prov = document.getElementById('pprovider').value;
  if (prov === 'spacexai'){
    const ok = confirm(
      'Opt in to SpaceXAI?\n\n' +
      'Chat text will leave this device for api.x.ai.\n' +
      'Memory files and embeddings stay local.\n' +
      'You can switch back to ollama anytime.'
    );
    if (!ok){
      document.getElementById('pprovider').value = 'ollama';
      return;
    }
  }
  await fetch('/api/profile/meta', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({avatar: document.getElementById('pavatar').value.trim(),
                          description: document.getElementById('pdesc').value.trim(),
                          model: document.getElementById('pmodel').value.trim(),
                          provider: prov,
                          cloud_opt_in: prov === 'spacexai'})});
  refreshProfiles();
};
document.getElementById('reflectbtn').onclick = async () => {
  const b = bubble('her', 'reflecting…');
  const r = await fetch('/api/reflect', {method:'POST'});
  const data = await r.json();
  b.textContent = data.insights;
  refreshMems();
};
document.getElementById('delprofile').onclick = async () => {
  const name = prompt('Delete which profile? (cannot be the active one — this erases its memory forever)');
  if (!name) return;
  if (!confirm(`Really delete profile "${name}" and all its memory? This cannot be undone.`)) return;
  const r = await fetch('/api/profile/delete', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({profile: name})});
  const data = await r.json();
  alert(data.ok ? `Profile "${name}" deleted.` : (data.error || 'Nothing deleted.'));
  refreshProfiles();
};
refreshProfiles(); refreshMems();
</script>
</body>
</html>"""


def _profile_of(companion: Clementine) -> str:
    p = Path(companion.memory_dir)
    return p.name if p.parent == Path(_profiles.PROFILES_DIR) else "default"


# The only names a loopback-bound server should ever answer to. A browser on a
# malicious page can be made to resolve some attacker-controlled domain to
# 127.0.0.1 (DNS rebinding) and then fetch http://127.0.0.1:<port>/… — the OS
# socket accepts it, but the browser still sends the *attacker's* domain in the
# Host header. Refusing any Host that isn't loopback closes that hole without
# any new dependency. See main()/create_app for how the port is supplied.
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "[::1]"})


def _host_is_local(host_header: str, port: int) -> bool:
    """True only for a loopback hostname with no port or the expected port."""
    h = (host_header or "").strip()
    if not h:
        return False
    if h.startswith("["):                       # IPv6 literal: [::1] or [::1]:5000
        end = h.find("]")
        if end == -1:
            return False
        hostname, rest = h[:end + 1], h[end + 1:]
        port_part = rest[1:] if rest.startswith(":") else ""
    else:
        name, sep, maybe_port = h.rpartition(":")
        if sep and maybe_port.isdigit():
            hostname, port_part = name, maybe_port
        else:
            hostname, port_part = h, ""
    if hostname not in _LOOPBACK_HOSTS:
        return False
    return not port_part or port_part == str(port)


def create_app(companion: Clementine, port: int = 5000) -> Flask:
    app = Flask(__name__)
    holder = {"c": companion}  # swapped in place when the profile changes

    @app.before_request
    def _reject_foreign_host():
        # Guards every route, including the private /api/expose dumps, against
        # DNS-rebinding reads from a malicious website. Loopback callers (the
        # human at their own machine) are unaffected.
        if not _host_is_local(request.host, port):
            abort(403, description="This companion answers on localhost only.")

    @app.get("/")
    def home():
        c = holder["c"]
        return render_template_string(
            PAGE, name=c.personality.name or "Clementine")

    @app.post("/api/chat")
    def chat():
        message = ((request.get_json(silent=True) or {}).get("message") or "").strip()
        if not message:
            return jsonify({"error": "empty message"}), 400
        return jsonify({"reply": holder["c"].chat(message)})

    @app.post("/api/chat/stream")
    def chat_stream():
        message = ((request.get_json(silent=True) or {}).get("message") or "").strip()
        if not message:
            return jsonify({"error": "empty message"}), 400
        return Response(holder["c"].chat_stream(message),
                        mimetype="text/plain; charset=utf-8",
                        headers={"X-Accel-Buffering": "no"})

    @app.get("/api/memories")
    def memories():
        return jsonify(holder["c"].list_memories())

    @app.post("/api/reflect")
    def reflect():
        return jsonify({"insights": holder["c"].reflect()})

    @app.post("/api/teach")
    def teach():
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        key = (data.get("key") or "").strip()
        if not text:
            return jsonify({"ok": False, "error": "empty"}), 400
        if key:
            holder["c"].remember_fact(key, text)
        else:
            holder["c"].remember(text)
        return jsonify({"ok": True})

    @app.post("/api/forget")
    def forget():
        handle = ((request.get_json(silent=True) or {}).get("handle") or "").strip()
        forgotten = holder["c"].forget(handle)
        return jsonify({"ok": bool(forgotten), "forgotten": forgotten})

    @app.get("/api/profile")
    def profile_get():
        c = holder["c"]
        current = _profile_of(c)
        names = list_profiles()
        if current not in names:
            names = [current] + names
        profiles = []
        for n in names:
            if n == current:
                profiles.append({"profile": n,
                                 "avatar": c.personality.avatar,
                                 "description": c.personality.description,
                                 "name": c.personality.name,
                                 "model": c.model,
                                 "provider": c.provider})
            elif n == "default":
                profiles.append({"profile": n, "avatar": "",
                                 "description": "", "name": "", "model": "",
                                 "provider": ""})
            else:
                meta = profile_meta(n)
                profiles.append(meta)
        from crystalcore import xai_api_key_present
        return jsonify({
            "current": current,
            "profiles": profiles,
            "provider": c.provider,
            "model": c.model,
            "active_provider": c.active_chat_provider(),
            "active_model": c.active_chat_model(),
            "local_fallback": c.spacexai_using_local_fallback(),
            "cloud_opt_in": bool(c.personality.cloud_opt_in),
            "cloud_opt_in_at": c.personality.cloud_opt_in_at or "",
            "xai_key_present": xai_api_key_present(),
        })

    @app.post("/api/profile/meta")
    def profile_meta_set():
        data = request.get_json(silent=True) or {}
        c = holder["c"]
        if "avatar" in data:
            c.personality.avatar = str(data["avatar"]).strip()[:8]
        if "description" in data:
            c.personality.description = str(data["description"]).strip()[:200]
        if "provider" in data and str(data["provider"]).strip():
            c.set_provider(str(data["provider"]))
        if "model" in data and str(data["model"]).strip():
            # set_model may re-opt-in if tag is grok-*; after set_provider is fine
            c.set_model(str(data["model"]))
        c.save()
        return jsonify({
            "ok": True,
            "provider": c.provider,
            "model": c.model,
            "cloud_opt_in": bool(c.personality.cloud_opt_in),
            "cloud_opt_in_at": c.personality.cloud_opt_in_at or "",
        })

    @app.post("/api/profile/delete")
    def profile_delete():
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        if name == _profile_of(holder["c"]):
            return jsonify({"ok": False,
                            "error": "switch away before deleting the active profile"}), 400
        return jsonify({"ok": delete_profile(name)})

    @app.post("/api/profile")
    def profile_switch():
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        try:
            target = profile_dir(name)
        except ValueError:
            return jsonify({"ok": False, "error": "invalid name"}), 400
        old = holder["c"]
        # Do not pass the previous profile's provider — the target folder's
        # config.json (and model heuristics) decide the backend.
        holder["c"] = Clementine(memory_dir=target,
                                 embed_model=old.embed_model)
        c = holder["c"]
        from crystalcore import xai_api_key_present
        return jsonify({
            "ok": True,
            "profile": _profile_of(c),
            "name": c.personality.name or "Clementine",
            "provider": c.provider,
            "model": c.model,
            "cloud_opt_in": bool(c.personality.cloud_opt_in),
            "cloud_opt_in_at": c.personality.cloud_opt_in_at or "",
            "xai_key_present": xai_api_key_present(),
        })

    # ----- full transparency (localhost only; never leave the device) -----

    @app.get("/api/expose")
    @app.get("/api/system")
    def expose_all():
        """Everything: package, memory, conversation, node, routes, prompts."""
        return jsonify(full_expose(companion=holder["c"]))

    @app.get("/api/conversation")
    def conversation():
        c = holder["c"]
        return jsonify({
            "conversation": c.memory.conversation,
            "summaries": c.memory.summaries,
            "last_seen": c.memory.last_seen,
            "count": len(c.memory.conversation),
        })

    @app.get("/api/prompt")
    def prompt():
        c = holder["c"]
        q = (request.args.get("q") or "").strip()
        from crystalcore.companion import (
            BASE_PROMPT_LOCAL,
            BASE_PROMPT_SPACEXAI,
            PROVIDER_SPACEXAI,
        )
        base = (BASE_PROMPT_SPACEXAI
                if getattr(c, "provider", "") == PROVIDER_SPACEXAI
                else BASE_PROMPT_LOCAL)
        return jsonify({
            "base_prompt": base,
            "provider": getattr(c, "provider", "ollama"),
            "system_prompt_live": c.system_prompt(q),
            "personality": companion_dump(c, include_prompt=False)["personality"],
        })

    return app


def main():
    import os
    from crystalcore import load_dotenv, xai_api_key_present

    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Clementine's local web interface (127.0.0.1 only).")
    parser.add_argument("--model", default="llama3.1:8b",
                        help="Model id (Ollama tag or grok-* for SpaceXAI).")
    parser.add_argument("--provider", default="",
                        help="ollama (local) or spacexai (opt-in; XAI_API_KEY).")
    parser.add_argument("--memory-dir", default="clementine_memory",
                        help="Her memory folder (shared with the CLI).")
    parser.add_argument("--profile", default="",
                        help="Named profile (separate person, separate memory).")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    provider = (args.provider or os.environ.get("CRYSTAL_PROVIDER", "")).strip()
    companion = Clementine(model=args.model, memory_dir=args.memory_dir,
                           provider=provider)
    app = create_app(companion, port=args.port)
    name = companion.personality.name or "Clementine"
    print(f"{name} is at home: open http://127.0.0.1:{args.port}")
    if companion.spacexai_using_local_fallback():
        print(f"SpaceXAI opted in but no XAI_API_KEY — local FALLBACK "
              f"({companion.active_chat_model()}).")
        print("Add key to .env (https://console.x.ai). UI: 127.0.0.1 only.")
    elif companion.provider == "spacexai":
        print(f"SpaceXAI chat ({companion.model}) — memory stays local. "
              "UI still binds 127.0.0.1 only.")
    else:
        print("Local only — chat via Ollama. Ctrl+C to say goodnight.")
    # Never bind beyond localhost, never enable the debugger: the UI is
    # reachable from this machine alone (chat may leave if SpaceXAI is on).
    # threaded=True so a long SpaceXAI stream does not freeze the whole UI.
    app.run(host="127.0.0.1", port=args.port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
