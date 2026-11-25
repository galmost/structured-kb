# Pi Coding Agent Harness with Mistral (Debian 13)

[Pi](https://pi.dev) (badlogic pi-coding-agent) is terminal agent with `read`/`bash`/`edit`/`write`. Note install user-local, make hosted **Mistral** API default (native provider, login `pi auth login mistral`), register local [Avalon](../amd/avalon/README.md) and qwen-coder `llama-server` as OpenAI-compatible providers in `models.json`.

User config in `~/.pi/agent/` (override `PI_CODING_AGENT_DIR`). Project config in `.pi/` under work dir, load only after trust.

## 1. Prerequisites

- Debian 13 (trixie), Node.js 24 from NodeSource (see [Node.js Setup](../../nodejs/README.md)), `~/.local/bin` first on `PATH`.
- Local providers: `avalon-server` on http://127.0.0.1:8080 (`sg render -c 'avalon-server -c 65536'`, see Avalon note), optional `qwen-coder-server` on http://127.0.0.1:8081 (wrapper `~/.local/bin`, default `-c 32768`).
- Mistral account for `pi auth login mistral` (browser OAuth or API key).

## 2. Install

npm global prefix `/usr` is root-owned; install user-local, put `pi` in `~/.local/bin`:

```bash
npm install -g --prefix ~/.local --ignore-scripts @earendil-works/pi-coding-agent
pi --version    # 1.5.2
```

`@mariozechner/pi-coding-agent` is legacy (stuck 0.73.1) — use `@earendil-works/pi-coding-agent`. `--ignore-scripts` skip lifecycle scripts, pi not need.

## 3. Authenticate to Mistral (hosted)

Pi hide model list until credentials; until then `pi --list-models mistral` print `No models available`, startup warn `No models match pattern "mistral/..."`, `pi auth check --provider mistral` report `not_ready` (`credentials_not_configured`). Expected, not error.

Pick one sign-in — need browser approval or API key from https://console.mistral.ai "API keys":

```bash
pi auth login mistral                    # browser OAuth; --no-browser uses a device code instead
pi auth login mistral --api-key          # paste an API key instead of browser sign-in
pi auth check --provider mistral         # ready
pi --list-models mistral                 # mistral-large-latest, devstral-latest, codestral-latest, ...
```

Credentials in `~/.pi/agent/auth.json` — never commit (home_config `.gitignore` default-deny, stays untracked; see section 6). CI alternative, no `auth.json` write: `export MISTRAL_API_KEY=...` before start pi (e.g. via `~/.config/environment.d/`).

## 4. Harness files in `~/.pi/agent/`

`settings.json` — default model plus per-model thinking:

```json
{
  "$schema": "https://pi.dev/schemas/settings.schema.json",
  "defaultProvider": "mistral",
  "defaultModel": "mistral-large-latest",
  "defaultThinkingLevel": "medium",
  "enabledModels": [
    "mistral/mistral-large-latest",
    "mistral/devstral-latest",
    "avalon/*",
    "qwen-coder/*"
  ],
  "modelThinkingLevels": {
    "avalon/Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf": "low",
    "qwen-coder/qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf": "medium"
  }
}
```

`models.json` — local OpenAI-compatible providers (dummy `apiKey`; llama-server ignore auth):

```json
{
  "$schema": "https://pi.dev/schemas/models.schema.json",
  "providers": {
    "avalon": {
      "baseUrl": "http://127.0.0.1:8080/v1",
      "api": "openai-completions",
      "apiKey": "avalon",
      "models": [
        {
          "id": "Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf",
          "name": "avalon (Qwen3.8-Flash-Next, local)",
          "reasoning": true,
          "contextWindow": 65536,
          "maxTokens": 8192
        }
      ]
    },
    "qwen-coder": {
      "baseUrl": "http://127.0.0.1:8081/v1",
      "api": "openai-completions",
      "apiKey": "qwen-coder",
      "models": [
        {
          "id": "qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf",
          "name": "qwen2.5-coder-7b (local)",
          "reasoning": true,
          "contextWindow": 32768,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

- Model `id` must match `curl http://127.0.0.1:8080/v1/models` exactly.
- Avalon chat template only accept reasoning effort `xhigh` (default), `medium`, `low` — hence `"low"` in `modelThinkingLevels`.

`AGENTS.md` — user-level instructions in every project:

```markdown
# Global pi instructions

- This machine's knowledge base lives in `~/git/structured-kb`. When working
  in that repo, follow its `AGENTS.md` conventions: one topic folder per note,
  `docs(kb):` conventional commits on `docs/` branches, never push to `main`.
- `~` is the `home_config` git worktree (Bitbucket). Only allowlisted dotfiles
  are tracked — never commit secrets: `~/.pi/agent/auth.json`, SSH private
  keys, browser profiles, shell histories.
- In non-interactive shells on Debian 13 prefer `pkexec` over `sudo` (sudo
  prompts for a password; pkexec authenticates via polkit).
- Local LLM servers: `avalon-server` on http://127.0.0.1:8080 (see
  `~/git/structured-kb/computer/debian/ai/amd/avalon/README.md`), registered
  in `models.json` as provider `avalon`.
```

Project `.pi/` mirror layout (`settings.json`, `mcp.json`, `SYSTEM.md`, `APPEND_SYSTEM.md`, `extensions/`, `skills/`, `prompts/`, `themes/`) load after trust project (`--approve` / `--no-approve`). `SYSTEM.md` replace system prompt, `APPEND_SYSTEM.md` append; trusted project file win over agent-dir file same name. Example in git: `Avalon/.pi/gg/APPEND_SYSTEM.md` tracked, `Avalon/.pi/SYSTEM.md` gitignored (generated).

## 5. Verify

```bash
pi --list-models avalon
# avalon  Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf  65.5K  8.2K  yes  no

cd ~
pi -p 'Reply with exactly: pong' --model 'avalon/Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf' --thinking low --no-session
# pong    (verified)

pi -p 'Reply with exactly: pong'    # after `pi auth login mistral`: uses default mistral/mistral-large-latest
```

`-p` one-shot (print answer, exit); `--no-session` skip session storage. `--model` accept `provider/id` and optional `:thinking` suffix.

## 6. Tracking the harness in home_config

`~` is home_config worktree with default-deny `.gitignore` (`*` then allowlist). Allowlist only non-secret harness files:

```bash
# ~/.gitignore
!.pi/
!.pi/agent/
!.pi/agent/AGENTS.md
!.pi/agent/models.json
!.pi/agent/settings.json
```

`git status` in `~` show only those three files; `auth.json`, sessions, logs stay ignored. Verify `git check-ignore -v ~/.pi/agent/auth.json`.

## 7. Caveman skill (terse output)

`~/AGENTS.md` load `caveman` skill at start of every pi run, so pi answer terse until user say "stop caveman" or "normal mode". Pi discover user skills from `<agent-dir>/skills/`, i.e. `~/.pi/agent/skills/` (see section 4). Install skill as directory with `SKILL.md`:

```bash
mkdir -p ~/.pi/agent/skills/caveman
# write ~/.pi/agent/skills/caveman/SKILL.md
```

`SKILL.md` is Agent Skills form of caveman voice rules (answer first, no ceremony, payload verbatim, one idea per sentence), commands adapted to pi: `/skill:caveman` instead of `/caveman`, so `/skill:caveman status`, `/skill:caveman ultra` etc. work. Source copy at `~/.vibe/skills/caveman/SKILL.md` (Vibe harness). Pi advertise skill by name and description at startup, load full instructions on demand; force with `/skill:caveman`, reload after edits with `/reload`.

Track skill in home_config by extend `.pi` allowlist in `~/.gitignore` (section 6):

```bash
# ~/.gitignore
!.pi/agent/skills/
!.pi/agent/skills/**
```

Verify:

```bash
ls ~/.pi/agent/skills/caveman/SKILL.md
pi -p 'Say exactly: pong' --no-session   # skill listed in startup diagnostics
# in an interactive session: /skill:caveman  -> terse replies from then on
```

See [README-skills.md](README-skills.md) for full user-skills layout, including `caveman-compress` skill.

## Troubleshooting

- `not_ready` from `pi auth check --provider mistral` — run `pi auth login mistral` first.
- `Warning: No models match pattern "mistral/..."` at startup — Mistral not logged in yet; local providers unaffected.
- `connection refused` on 127.0.0.1:8080 — avalon-server not running: `sg render -c 'avalon-server -c 65536'`. While busy, requests queue: `curl http://127.0.0.1:8080/slots` show `"is_processing": true`.
- Model not listed by `pi --list-models avalon` — `id` in `models.json` not match `/v1/models`; fix string.
- `Jinja Exception: Unexpected reasoning effort ...` — thinking level outside xhigh/medium/low; use `--thinking low` or set `modelThinkingLevels`.
- `npm error ... permissions` on `npm install -g` — add `--prefix ~/.local`.
- Project `.pi/` files not loaded — project not trusted; start pi with `--approve` (or accept trust prompt).

## Source

- [Pi docs — Configuration](https://pi.dev/docs/latest/configuration)
- [Pi docs — Choose a Model / models.json](https://pi.dev/docs/latest/models)
- [Pi docs — Settings reference](https://pi.dev/docs/latest/settings)
- [Pi docs — Providers (MISTRAL_API_KEY)](https://pi.dev/docs/latest/providers)
- [Pi docs — Skills](https://pi.dev/docs/latest/skills)
- [pi-mono on GitHub](https://github.com/badlogic/pi-mono)
- [npm: @earendil-works/pi-coding-agent](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
- [Avalon note in this repo](../amd/avalon/README.md)
- [Mistral Vibe note in this repo](../mistral/README.md)