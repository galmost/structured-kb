# Caveman CLI for Pi (Assessment)

`@caveman-ai/cli` v4.2.0 wraps 30+ agents with compression, metering and Auto mode. Pi is **not** supported (OMP is a different tool), so the skills route is the Pi answer.

## 1. Install

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent   # optional: skip postinstall
npm install -g @caveman-ai/cli                                    # or: npx @caveman-ai/cli@latest
```

Needs Node.js 22.13+ and npm.

## 2. Supported agents

| Agent | Command |
|-------|---------|
| Claude Code | `caveman claude` |
| Codex | `caveman codex` |
| Gemini | `caveman gemini` |
| OpenCode | `caveman opencode` |
| OMP | `caveman omp` |
| Copilot | `caveman copilot` |

Pi not listed. `caveman pi` fails or passes through.

## 3. CLI vs Skills

| Feature | Skills | CLI |
|---------|--------|-----|
| Caveman voice | ✅ | ✅ |
| Input compression | ❌ | ✅ 33.2% |
| Auto mode | ❌ | ✅ 0.46x cost |
| Blocks | ❌ | ✅ 397→76 |
| Metering/dashboard | ❌ | ✅ |
| Pi support | ✅ | ❌ |
| Deps | None | Node 22.13+, Go binaries |

## 4. Recommendation

- **Pi only**: Skills (current setup). Simple, native.
- **Multi-agent**: CLI for the other agents, skills for Pi.
- **Experimental**: `caveman pi` may not work — debugging expected.

## Verify

```bash
caveman setup
```

Skills-side mode check: `/caveman status` in Pi.

## Source

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
