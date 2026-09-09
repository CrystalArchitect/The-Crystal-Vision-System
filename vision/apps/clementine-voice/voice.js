// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

/**
 * Local voice via the browser's speech synthesis. Only on-device voices are
 * used (localService === true), so speaking never hands text to a network TTS
 * server — nothing leaves the machine. If the device has no on-device voice,
 * they stay silent rather than fall back to a cloud voice and break that promise.
 */

const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;

export function voiceSupported() {
  return supported;
}

/** On-device voices only — network/cloud voices are excluded by design. */
export function listVoices() {
  if (!supported) return [];
  return window.speechSynthesis.getVoices().filter((v) => v.localService);
}

export function onVoicesChanged(cb) {
  if (supported) window.speechSynthesis.addEventListener('voiceschanged', cb);
}

export function speak(text, voiceName = '') {
  if (!supported) return;
  const clean = text.replace(/\s+/g, ' ').trim();
  if (!clean) return;
  const local = listVoices();
  // Bind an on-device voice explicitly (the chosen one if it's local, else the
  // first local voice). Never leave it to a browser default that might be a
  // network voice; if there is no local voice at all, do not speak.
  const voice = local.find((x) => x.name === voiceName) || local[0];
  if (!voice) return;
  const u = new SpeechSynthesisUtterance(clean);
  u.voice = voice;
  window.speechSynthesis.speak(u);
}

export function stopSpeaking() {
  if (supported) window.speechSynthesis.cancel();
}
