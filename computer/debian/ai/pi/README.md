# Pi Coding Agent Harness with Mistral (Debian 13)

[Pi](https://pi.dev) (badlogic pi-coding-agent) is a terminal coding agent with
`read`/`bash`/`edit`/`write` tools. This note installs it user-local, makes the
hosted **Mistral** API the default model (native provider, login via
`pi auth login mistral`), and registers the local
[Avalon](../amd/avalon/README.md) and qwen-coder `llama-server` instances as
OpenAI-compatible providers in `models.json`.

User-level configuration lives in the agent directory `~/.pi/agent/` (override
with the `PI_CODING_AGENT_DIR` environment variable). Project-level config lives
in `.pi/` under the working directory and loads only after the project is trusted.

## 1. Prerequisites

- Debian 13 (trixie), Node.js 24 from NodeSource (see
  [Node.js Setup](../../nodejs/README.md)) with `~/.local/bin` first on `PATH`.
- For the local providers: `avalon-server` on http://127.0.0.1:8080
  (`sg render -c 'avalon-server -c 65536'`, see the Avalon note) and optionally
  `qwen-coder-server` on http://127.0.0.1:8081 (wrapper in `~/.local/bin`,
  default `-c 32768`).
- A Mistral account for `pi auth login mistral` (browser OAuth or API key).

## 2. Install

The npm global prefix `/usr` is root-owned, so install user-local — this puts
`pi` in `~/.local/bin`:

```bash
npm install -g --prefix ~/.local --ignore-scripts @earendil-works/pi-coding-agent
pi --version    # 1.5.2
```

`@mariozechner/pi-coding-agent` is the legacy package name (stuck at 0.73.1) —
use `@earendil-works/pi-coding-agent`. `--ignore-scripts` skips dependency
lifecycle scripts, which pi does not need.

## 3. Authenticate to Mistral (hosted)

```bash
pi auth login mistral               # browser OAuth or paste an API key; saved to ~/.pi/agent/auth.json
pi auth check --provider mistral   # ready
```

`auth.json` holds credentials — never commit it (the home_config `.gitignore` is
default-deny, so it stays untracked; see section 6). Alternative for CI:
`export MISTRAL_API_KEY=...` before starting pi.

Until login, `pi --list-models mistral` prints `No models available` and startup
warns `No models match pattern "mistral/..."` — expected, not an error.

## 4. Harness files in `~/.pi/agent/`

`settings.json` — default model plus per-model thinking levels:

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

`models.json` — local OpenAI-compatible providers (dummy `apiKey`; llama-server
ignores authentication):

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
- The Avalon chat template only accepts reasoning effort `xhigh` (default),
  `medium`, `low` — hence `"low"` in `modelThinkingLevels`.

`AGENTS.md` — user-level instructions applied in every project:

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

Project-level `.pi/` mirrors this layout (`settings.json`, `mcp.json`,
`SYSTEM.md`, `APPEND_SYSTEM.md`, `extensions/`, `skills/`, `prompts/`,
`themes/`) and loads after you trust the project (`--approve` / `--no-approve`
on the CLI). `SYSTEM.md` replaces the system prompt, `APPEND_SYSTEM.md` appends
to it; a trusted project file takes precedence over the agent-directory file of
the same name. Example already in git: `Avalon/.pi/gg/APPEND_SYSTEM.md` is
tracked, while `Avalon/.pi/SYSTEM.md` is gitignored because it is generated.

## 5. Verify

```bash
pi --list-models avalon
# avalon  Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf  65.5K  8.2K  yes  no

cd ~
pi -p 'Reply with exactly: pong' --model 'avalon/Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf' --thinking low --no-session
# pong    (verified)

pi -p 'Reply with exactly: pong'    # after `pi auth login mistral`: uses default mistral/mistral-large-latest
```

`-p` is one-shot mode (print answer and exit); `--no-session` skips session
storage. `--model` accepts `provider/id` and an optional `:thinking` suffix.

## 6. Tracking the harness in home_config

`~` is the home_config worktree with a default-deny `.gitignore` (`*` then an
allowlist). Allowlist only the non-secret harness files by appending:

```bash
# ~/.gitignore
!.pi/
!.pi/agent/
!.pi/agent/AGENTS.md
!.pi/agent/models.json
!.pi/agent/settings.json
```

`git status` in `~` then shows only those three files; `auth.json`, sessions and
logs stay ignored. Verify with `git check-ignore -v ~/.pi/agent/auth.json`.

## Troubleshooting

- `not_ready` from `pi auth check --provider mistral` — run
  `pi auth login mistral` first.
- `Warning: No models match pattern "mistral/..."` at startup — Mistral is not
  logged in yet; local providers are unaffected.
- `connection refused` on 127.0.0.1:8080 — avalon-server is not running:
  `sg render -c 'avalon-server -c 65536'`. While the server is busy, requests
  queue: `curl http://127.0.0.1:8080/slots` shows `"is_processing": true`.
- Model not listed by `pi --list-models avalon` — the `id` in `models.json` does
  not match `/v1/models`; fix the string.
- `Jinja Exception: Unexpected reasoning effort ...` — thinking level outside
  xhigh/medium/low; use `--thinking low` or set `modelThinkingLevels`.
- `npm error ... permissions` on `npm install -g` — add `--prefix ~/.local`.
- Project `.pi/` files not loaded — the project is not trusted; start pi with
  `--approve` (or accept the trust prompt).

## Source

- [Pi docs — Configuration](https://pi.dev/docs/latest/configuration)
- [Pi docs — Choose a Model / models.json](https://pi.dev/docs/latest/models)
- [Pi docs — Settings reference](https://pi.dev/docs/latest/settings)
- [Pi docs — Providers (MISTRAL_API_KEY)](https://pi.dev/docs/latest/providers)
- [pi-mono on GitHub](https://github.com/badlogic/pi-mono)
- [npm: @earendil-works/pi-coding-agent](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
- [Avalon note in this repo](../amd/avalon/README.md)
- [Mistral Vibe note in this repo](../mistral/README.md)
