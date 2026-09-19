# Celestial Portal — Full Product Bill and Architecture Handoff

## Executive summary

**Celestial Portal** is intended to be the sovereign, multimodal AI entry point for **CrystalCore.OS**, owned by **TerAustralis Incognita**. The product direction is broader than a chatbot: it is a local-first creative, developer, social, entertainment, automation, and agent platform that can route work across local models, consented cloud providers, APIs, MCP tools, social networks, and media systems.

The current implementation is a **high-fidelity frontend concept and interaction prototype**, not a production AI platform. The visual web entry is now aligned to the supplied Celestial Portal artwork and brand direction. Core backend orchestration, real model execution, social integrations, billing, identity, multi-device sync, and production security still need to be architected and implemented.

## Current product identity

| Item | Decision |
|---|---|
| Company | TerAustralis Incognita |
| Product | CrystalCore.OS |
| Primary experience | Celestial Portal |
| Positioning | A sovereign multimodal AI operating environment, closer to an all-purpose creative and intelligence platform than a single chatbot |
| Visual language | Deep-space black, sapphire electric blue, violet nebula, crystal geometry, luminous energy, ceremonial serif typography |
| Default trust posture | Local-first, cloud only with explicit consent |
| Intended platforms | Web, iPhone, Android, Windows, macOS, and local/edge deployments |
| Intended audience | Creators, developers, operators, businesses, communities, and general users |

## What is actually built now

### 1. Reference-matched web entry

The current WebDev project is a React/Vite static frontend named `crystal-unified-developer-site`. The entry page now includes:

- Supplied Celestial Portal crystal-gateway artwork as the hero visual.
- Black starfield-style background treatment.
- Sapphire, electric blue, and violet gradients.
- Cinzel-style ceremonial serif branding for the portal identity.
- CrystalCore.OS attribution and TerAustralis Incognita footer attribution.
- “Enter the Celestial Portal” hero messaging.
- Local-first / cloud-consent positioning.
- Creation console for text, voice, image, and video modes.
- Social Orbit constellation.
- Entertainment Studio constellation.
- Live & Community constellation.
- API & Agents constellation.
- Consent policy entry point.
- Audit trace entry point.
- Voice Identity Vault entry point.

### 2. Multimodal composer prototype

The composer supports the following frontend states:

| Mode | Current behavior |
|---|---|
| Text | Prompt entry and simulated local result state |
| Voice | Prompt entry with voice-vault entry point |
| Image | Image-oriented prompt state and simulated result state |
| Video | Scene-oriented prompt state and simulated result state |

The composer also includes:

- Local vs cloud route selector.
- Cloud consent gate when policy requires explicit consent.
- Generation start and completion states.
- Local audit events for request and completion.
- Basic creation history cards.
- Responsive layout for desktop and mobile breakpoints.

**Important:** the current generation result is simulated UI behavior. No real LLM, image model, TTS engine, video model, queue, or provider router is connected to the composer yet.

### 3. Voice Identity Vault prototype

The project contains a substantial browser-side voice governance prototype:

- Explicit voice cloning consent state.
- Browser microphone capture using `MediaRecorder`.
- Playback of the captured recording.
- Simulated liveness and speaker matching flow.
- Model creation gate after consent and matching.
- Local encryption-sealing animation.
- Web Crypto SHA-256 fingerprints.
- IndexedDB persistence for encrypted recordings.
- Local decryption and fingerprint verification.
- Export/import migration bundles protected by a passphrase.
- Destination-device re-sealing.
- Duplicate-import suppression.
- Supplied Celestial Portal artwork in the model card.

**Important:** this is a browser prototype, not a certified biometric identity system. It must not be treated as legal, medical, security, or identity assurance until reviewed and rebuilt with platform secure enclaves, formal threat modeling, consent law review, and production key management.

### 4. Consent policy prototype

The consent policy editor currently exposes:

- Audit-log retention windows: 7, 30, 90, 365 days, or indefinite.
- Consent/revocation event retention toggle.
- Security/integrity event retention toggle.
- Explicit cloud-consent requirement.
- Biometric model creation permission.
- Local policy summary.
- Policy update audit event.
- Local-first storage messaging.

The policy service has been moved toward a versioned IndexedDB store with localStorage migration/fallback behavior.

**Important:** retention semantics still need architectural hardening. Filtering old events in the viewer is not the same as secure physical deletion, and chain verification must distinguish a complete chain from a retained/filtered chain.

### 5. Hash-chained audit viewer

The audit viewer currently includes:

- Local IndexedDB event storage.
- SHA-256 hash chaining.
- Previous-hash references.
- Event sequence numbers.
- Event categories and outcomes.
- Search.
- Category filtering.
- Refresh.
- Metadata export.
- Explicit local clear flow.
- Chain verification status.
- Privacy disclosures that exclude audio, voiceprints, keys, passphrases, ciphertext, and media payloads.
- Events for consent, connections, model activity, voice capture, migration, and policy changes.

**Important:** it is not yet a production-grade immutable audit system. Browser storage can be cleared or modified by the user or runtime. It provides local governance UX and tamper-evident behavior, not an externally witnessed compliance ledger.

## Current source structure

The important project files are:

```text
/home/ubuntu/crystal-unified-developer-site/
├── client/
│   ├── index.html
│   └── src/
│       ├── pages/
│       │   └── Home.tsx
│       ├── components/
│       │   ├── VoiceIdentityVault.tsx
│       │   ├── AuditLogViewer.tsx
│       │   ├── ConsentPolicyEditor.tsx
│       │   └── ui/                 # shadcn/Radix UI primitives
│       ├── lib/
│       │   ├── voiceVaultDb.ts
│       │   ├── auditLog.ts
│       │   ├── consentPolicy.ts
│       │   └── utils.ts
│       ├── contexts/
│       │   └── ThemeContext.tsx
│       ├── hooks/
│       ├── index.css
│       ├── main.tsx
│       └── const.ts
├── server/
│   └── index.ts                    # static serving placeholder
├── package.json
├── tsconfig.json
├── vite.config.ts
└── pnpm-lock.yaml
```

## What is not built yet

### AI and model infrastructure

- No actual model gateway.
- No model registry.
- No local model discovery or lifecycle manager.
- No provider abstraction.
- No inference queue.
- No token/cost accounting.
- No streaming responses.
- No context-window management.
- No multimodal input normalization.
- No fallback routing.
- No prompt or artifact versioning.
- No agent runtime.
- No tool permission broker.
- No model evaluation harness.

### Text and conversation experience

- No persistent conversations.
- No project/workspace database.
- No long-term memory policy.
- No retrieval-augmented generation.
- No citations or provenance graph.
- No document upload and indexing pipeline.
- No collaborative threads.
- No conversation export/import beyond the voice-vault migration flow.

### Voice

- No production speech-to-text provider.
- No production text-to-speech provider.
- No voice model hosting.
- No streaming audio pipeline.
- No speaker diarization.
- No production liveness or anti-spoofing.
- No platform-level secure key storage.
- No lawful voice consent workflow.
- No watermark verification service.

### Image

- No real image model adapter.
- No image generation queue.
- No image editing pipeline.
- No image asset store.
- No image history or variants database.
- No prompt-to-asset provenance.
- No safety/moderation pipeline.
- No seed/model/parameter reproducibility system.

### Video and music

- No video generation engine.
- No timeline editor.
- No scene graph.
- No render queue.
- No transcoding service.
- No caption/subtitle pipeline.
- No music generation engine.
- No stems, tracks, or project format.
- No publishing-ready encoding presets.

### Social and platform integrations

No production integrations are wired into the current web app. The product vision calls for a connector layer supporting, subject to user consent and platform policies:

- Instagram.
- YouTube.
- TikTok.
- X.
- LinkedIn.
- Facebook.
- Reddit.
- Discord.
- Telegram.
- Slack.
- Google Drive.
- GitHub.
- S3/object storage.
- OpenAI-compatible providers.
- MCP servers.
- Webhooks.
- RSS and publishing feeds.

Required capabilities include account linking, token rotation, scoped permissions, drafts, scheduling, publishing, analytics, comment/community workflows, media adaptation, and revocation.

### Product platform

- No account system.
- No organization/team model.
- No roles and permissions.
- No billing.
- No 42-tier entitlement enforcement.
- No usage quotas.
- No Stripe products/prices.
- No API keys.
- No developer portal.
- No production webhooks.
- No support/admin console.
- No data export/delete account workflows.
- No observability stack.
- No incident response system.
- No compliance controls.

### Native applications

There are no native iPhone, Android, Windows, or macOS applications in the current project. The frontend is web-only and static/client-side.

For the intended product, the recommended native architecture is:

- Web: React/Vite or Next-style frontend.
- iPhone/Android: Expo/React Native or platform-native shells around shared domain modules.
- Windows/macOS: Tauri or Electron only if the local edge requirements cannot be met by a secure native runtime.
- Local edge: a separately packaged service with encrypted storage, model runtime management, and explicit network policy.

## Recommended target architecture for Claude

### Layer 1 — Experience shell

- Celestial Portal web entry.
- Chat-first composer.
- Project/workspace navigation.
- Creator studio.
- Social Orbit.
- Entertainment Studio.
- Developer/API workspace.
- Consent and trust center.
- Admin and billing surfaces.

### Layer 2 — Domain model

Define shared domain types first:

```text
User
Organization
Workspace
Project
Conversation
Message
Artifact
GenerationJob
Model
Provider
Connector
ConsentPolicy
ConsentGrant
AuditEvent
UsageRecord
Entitlement
Publication
Campaign
Agent
Tool
```

Every artifact and generation job should carry:

- owner/workspace ID.
- source prompt or input reference.
- model/provider ID.
- route: local or cloud.
- consent grant reference.
- policy version.
- provenance metadata.
- lifecycle status.
- created/updated timestamps.

### Layer 3 — Capability router

Create one routing contract for all modalities:

```text
submitGeneration({
  workspaceId,
  modality: text | voice | image | video | music | code,
  input,
  requestedModel,
  routePreference: local | cloud | auto,
  consentContext,
  outputPolicy,
}) -> GenerationJob
```

The router must:

1. Validate entitlement.
2. Validate consent.
3. Select an available provider/model.
4. Estimate cost and resource use.
5. Create an auditable job.
6. Stream status.
7. Store output/provenance.
8. Support retry/fallback.
9. Apply retention and deletion rules.

### Layer 4 — Provider adapters

Use a stable adapter interface for:

- Local LLM.
- Cloud LLM.
- STT.
- TTS.
- Voice transformation.
- Image generation.
- Image editing.
- Video generation.
- Music generation.
- Embeddings.
- Moderation.

Do not make the UI know provider-specific request shapes.

### Layer 5 — Local edge runtime

The local runtime needs:

- Model installation and update management.
- Hardware capability detection.
- Process isolation.
- Encrypted local storage.
- Key management.
- Offline queues.
- Network egress policy.
- Local API endpoint.
- Health checks.
- Logs and diagnostics.
- Resource quotas.
- Safe shutdown/recovery.

### Layer 6 — Consent and trust plane

Consent must be a first-class service, not scattered UI booleans. It should answer:

```text
can(action, subject, dataClass, destination, purpose, policyVersion) -> decision
```

Examples:

- Can this prompt leave the device?
- Can this voice recording be used for model creation?
- Can this image be published to Instagram?
- Can this connector read repository contents?
- Can this agent invoke an external API?
- Can this artifact be retained for 90 days?

### Layer 7 — Social and entertainment orchestration

Add a platform-neutral content object:

```text
ContentAsset
  sourceArtifact
  variants[]
  destinationPlatforms[]
  captions[]
  schedules[]
  consentGrants[]
  publicationStatus[]
  analyticsLinks[]
```

This allows one creation to become:

- a long-form video.
- a short vertical cut.
- a thumbnail.
- a social caption.
- a voiceover.
- a transcript.
- a newsletter.
- a live-room prompt.
- a developer announcement.

### Layer 8 — Billing and 42-tier entitlement model

The 42 tiers need a real product specification before implementation:

- Tier names.
- Price.
- currency.
- included tokens/credits.
- generation limits.
- storage limits.
- connected accounts.
- team members.
- model access.
- local/cloud allocation.
- API rate limits.
- overage policy.
- cancellation/grace period.
- data retention defaults.

Use deny-by-default entitlement checks across UI, API, MCP, webhooks, SDK, CLI, and background jobs.

## Immediate build order

### Phase 0 — Architecture correction

1. Freeze the visual reference and brand tokens.
2. Decide web-first MVP boundaries.
3. Define domain types and storage model.
4. Define local edge vs cloud responsibilities.
5. Define consent decision contract.
6. Define provider adapter interfaces.
7. Decide whether local runtime is a separate service or desktop shell.

### Phase 1 — Real text assistant

1. User/workspace identity.
2. Conversation persistence.
3. Local model adapter.
4. Streaming responses.
5. Cloud provider adapter behind consent.
6. Conversation export.
7. Audit and provenance.

### Phase 2 — Real multimodal jobs

1. Unified generation jobs.
2. Real STT/TTS.
3. Image generation.
4. Video queue and preview.
5. Asset storage.
6. Job status/events.
7. Retry/fallback.

### Phase 3 — Social Orbit

1. Connector registry.
2. OAuth/token vault.
3. Scoped permissions.
4. Draft adaptation.
5. Scheduling.
6. Publishing.
7. Analytics.
8. Revocation and data deletion.

### Phase 4 — Entertainment Studio

1. Timeline/project model.
2. Scene graph.
3. Media asset browser.
4. Audio/music tracks.
5. Captions and voiceover.
6. Render queue.
7. Export presets.
8. Publishing variants.

### Phase 5 — Developers and agents

1. MCP registry.
2. API keys.
3. Tool permission broker.
4. Agent execution runtime.
5. Workflow builder.
6. Webhooks.
7. Logs and replay.
8. Usage controls.

### Phase 6 — Native and sovereign deployment

1. Package the local edge runtime.
2. Desktop shell.
3. Mobile companion apps.
4. Offline sync model.
5. Device trust and recovery.
6. Secure storage integration.
7. Multi-device consent synchronization.

## Honest status table

| Area | Status | Confidence |
|---|---|---|
| Celestial Portal visual direction | Built in frontend prototype | High |
| Supplied artwork integration | Built | High |
| Multimodal composer UI | Built as simulated frontend | High |
| Local/cloud consent UI | Built as frontend behavior | Medium |
| Consent policy editor | Built as browser prototype | Medium |
| Audit log viewer | Built as browser prototype | Medium |
| Voice capture/vault | Built as browser prototype | Medium |
| Real AI generation | Not built | High |
| Social integrations | Not built | High |
| Entertainment production pipeline | Not built | High |
| Billing/42 tiers | Not built | High |
| User accounts | Not built | High |
| Native apps | Not built | High |
| Sovereign local runtime | Not built | High |
| Production security/compliance | Not built | High |

## What Claude should fix first

Give Claude the following direction:

> Treat the current WebDev project as the visual product shell and interaction reference, not as the production architecture. Preserve the Celestial Portal visual identity and supplied artwork. Replace simulated generation with a domain-driven backend. Create a provider-neutral capability router, a first-class consent service, a local edge runtime boundary, durable project/conversation/artifact storage, and auditable generation jobs. Build the real text assistant first, then add voice, image, video, social publishing, entertainment workflows, MCP/API agents, billing, and native shells. Do not let UI booleans become the source of truth for permissions, entitlements, model routing, or retention.

## Current validation

The current project passes:

- `pnpm check`
- `pnpm build`
- live browser navigation.
- text composer interaction.
- image/video mode switching.
- responsive mobile screenshot verification.
- visual reference screenshot verification.

The current project is suitable as a **design handoff and frontend reference**, not as a production deployment of the full Celestial Portal product.

## Current website checkpoint

[Open the current Celestial Portal web entry](manus-webdev://35a0d148)
