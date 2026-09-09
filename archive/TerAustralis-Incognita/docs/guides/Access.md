# Access & Invite List

**Keeper:** Crystal (CrystalArchitect)
**This repo is public.** So are `-Code`, the proposal, and Clementine.
Private memory (Ollama, Clementine profiles, minted guest tokens) is
not. A URL is not a key.

The 2026-07 Windows laptop path in earlier revisions is retired.

---

## How people get in

| Audience | Path | What they get |
|----------|------|----------------|
| **You** | Local disk + Ollama + Bridge | Full house |
| **Guest AIs** | MCP CrystalBridge, after `--mint-token` | status / recall / teach / messages only |
| **Human collaborators** | GitHub (public clone) + sites + Discord you already share | Read the public plant. PRs. **Not** private memory |
| **GitHub org collaborator** | Maintainer click on repo Settings → Collaborators | Write on that repo, if you grant it |
| **Public** | [www](https://www.teraustralis.com.au), [proposal](https://proposal.teraustralis.com.au), public GitHub | What is already published |
| **External engine** | Recognition only ([ADR-0016](../adr/ADR-0016.md)) | No token. No tools. No memory |

Sending someone the GitHub org URL, the sites, and Discord **is** the
human door. It is not a GitHub Write invite, not OAuth, not a new
repository, and not a CrystalBridge mint.

Join path that is **refused** (same reasons as ADR-0015 / hybrid
identity): a twentieth GitHub, OAuth as login, a microservices rewrite,
a second Discord “for the project.”

---

## GitHub collaborator invites (human)

Public clone needs no invite. Write on a repo is a maintainer click:

1. Open the **named living repo** → Settings → Collaborators
   (example: [umbrella access](https://github.com/CrystalArchitect/TerAustralis-Incognita/settings/access))
2. **Add people** → GitHub username
3. Permission: **Read** first. **Write** only when you want them
   pushing branches. Merge stays yours.

Agents do not click this. Grok Build does not click this.

### Invite roster

| GitHub user | Role | Permission | Org invite | Notes |
|-------------|------|------------|------------|-------|
| [MagisterJericoh](https://github.com/MagisterJericoh) | offered builder | none yet | ⬜ | 2026-08-20 Crystal sent GitHub, websites, Discord on X ([thread](https://x.com/magisterjericoh/status/2090207551317217779)). Public clone is enough to read. Write is a later click. No CrystalBridge mint. No OAuth. |

---

## Grok MCP (guest AI access) — wired

Guest AIs are not humans. Humans do not get a mint because they asked
nicely on Discord.

User config `~/.grok/config.toml` and project `.grok/config.toml`:

- Server name: **crystalbridge**
- Guest id: `CRYSTALBRIDGE_GUEST=grok`
- Command: Python `-m crystalcore.bridge --profile default` from
  [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)

**New Grok sessions** pick up MCP after config change (restart CLI if tools missing).

```
grok mcp list
# Tools should include crystalbridge__status, __recall, __teach, etc.
```

---

## Claude / Cursor guests

Same MCP command pattern as Grok; set `CRYSTALBRIDGE_GUEST=claude`
(or `cursor`). Approve them in the Code tree
`src/profiles/default/bridge_config.json` after a mint. Claude Code is
history ([ADR-0014](../adr/ADR-0014.md)).

---

## Quick links to send a human

- [www.teraustralis.com.au](https://www.teraustralis.com.au)
- [proposal.teraustralis.com.au](https://proposal.teraustralis.com.au)
- [Prototypes](https://proposal.teraustralis.com.au/prototypes.html)
- [Sydney Station](https://proposal.teraustralis.com.au/sydney-station.html)
- Engine: [TerAustralis-Incognita-Code](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)
- How to PR: [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
- Thirty-day software look-see: [evaluation licence](https://proposal.teraustralis.com.au/evaluation-license.html)

Discord stays the channel you already share. Do not publish invite
URLs in this file.

---

## External peers (not GitHub collaborators, not MCP guests)

| Peer | Path | What they get |
|------|------|----------------|
| [samuelsalmon3/SourceCode](https://github.com/samuelsalmon3/SourceCode) | Documented neighbor ([`ADR-0016`](../adr/ADR-0016.md), [peer card](../architecture/peers/SourceCode.md)) | Recognition only. No CrystalBridge token. No memory. No tools. |

A mint (`--mint-token`) is a maintainer act. Until then the gate is closed.
