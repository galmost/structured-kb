# Caveman CLI for Pi (Assessment)

`@caveman-ai/cli` v4.2.0 wraps 30+ agents with compression, metering, Auto. Pi not supported (OMP is, different tool). Skills approach recommended for Pi.

## 1. Prerequisites

- Node.js 22.13+
- npm
- Pi installed (see [Pi Setup](../../))

## 2. Pi Update

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

`--ignore-scripts` skips postinstall. Optional, safe for upgrades.

## 3. CLI Install

```bash
npm install -g @caveman-ai/cli
# or: npx @caveman-ai/cli@latest
```

## 4. Supported Agents

| Agent | Command |
|-------|---------|
| Claude Code | `caveman claude` |
| Codex | `caveman codex` |
| Gemini | `caveman gemini` |
| OpenCode | `caveman opencode` |
| OMP | `caveman omp` |
| Copilot | `caveman copilot` |

Pi not listed. `caveman pi` fails or pass-through.

## 5. CLI vs Skills

| Feature | Skills | CLI |
|---------|--------|-----|
| Caveman voice | ✅ | ✅ |
| Input compression | ❌ | ✅ 33.2% |
| Auto mode | ❌ | ✅ 0.46x cost |
| Blocks | ❌ | ✅ 397→76 |
| Metering/dashboard | ❌ | ✅ |
| Pi support | ✅ | ❌ |
| Deps | None | Node 22.13+, Go binaries |

## 6. Recommendation

- **Pi only**: Skills (current setup). Simple, native.
- **Multi-agent**: CLI for others + skills for Pi.
- **Experimental**: `caveman pi` may not work. Debug expected.

## Verify

```bash
/caveman status
caveman setup
```

## Source

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
