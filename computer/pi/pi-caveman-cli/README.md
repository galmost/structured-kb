# Pi Caveman CLI Integration Assessment

Assessment of using `@caveman-ai/cli@latest` with Pi coding agent, including `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` update.

## 1. Prerequisites

- Node.js 22.13+ (required by caveman CLI)
- npm or yarn
- Pi coding agent installed (see [Pi Coding Agent Setup for Linux](../../linux/pi/) or [Arch-specific guide](../../arch/pi/))

## 2. Update Pi

Reinstall Pi globally, skipping post-install scripts:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

**What it does**:
- Reinstalls Pi from npm
- `--ignore-scripts` skips `postinstall`, `preinstall`, `postuninstall` scripts
- Safe for upgrade, but may miss runtime setup if scripts perform critical initialization

**Note**: Pi typically installs via `npm install -g @earendil-works/pi-coding-agent` without `--ignore-scripts`. The flag is optional and mainly useful if post-install scripts fail or are unwanted.

## 3. Caveman CLI Installation

```bash
npx @caveman-ai/cli@latest
```

Or install globally:

```bash
npm install -g @caveman-ai/cli
```

**Version**: 4.2.0 (as of Nov 2026)
**License**: Apache-2.0
**Repository**: https://github.com/JuliusBrussee/caveman

## 4. Supported Agents

Caveman CLI supports 30+ agents via `caveman <agent>`:

| Agent | Command | Auto-activates |
|-------|---------|----------------|
| Claude Code | `caveman claude` | Yes |
| Codex CLI | `caveman codex` | Yes |
| Gemini CLI | `caveman gemini` | Yes |
| OpenCode | `caveman opencode` | Yes |
| Kilo Code | `caveman kilo` | Yes |
| **Oh My Pi (OMP)** | `caveman omp` | Yes |
| GitHub Copilot | `caveman copilot` | Yes |

**Note**: Pi (pi-coding-agent) is NOT in the official list. OMP (Oh My Pi) is supported, but this is a different tool.

## 5. Attempting to Wrap Pi

Since Pi is not officially supported, wrapping may not work out-of-the-box:

```bash
# Try wrapping Pi
caveman pi
```

**Expected behavior**: 
- CLI attempts to detect Pi installation
- If Pi not in supported list, may fail or fall back to pass-through
- No compression/metering applied

**Workaround**: Use skills approach (already implemented) instead of CLI wrap.

## 6. Assessment: CLI vs Skills

### Caveman CLI Approach

**Pros**:
- One install, all agents
- Local compression: 33.2% input token reduction
- Auto mode: 0.46x Opus cost
- Blocks: 397→76 tokens for test runs
- Truthful metering
- Offline dashboard (`caveman stats`)
- Token waste analysis (`caveman learn`)
- Web page compression (`caveman browse`)
- Tool catalog compression (`caveman tools compress catalog`)

**Cons**:
- Pi not officially supported
- Requires Node.js 22.13+
- Requires Go companion binaries
- Heavy installation (~100MB+)
- Complex setup for non-standard agents

### Skills Approach (Current)

**Pros**:
- Native Pi integration
- Lightweight (only skill files)
- No additional dependencies
- Works immediately
- Follows Pi's skill system

**Cons**:
- No input compression (Read less)
- No Auto mode
- No Blocks
- No metering/dashboard
- No token waste analysis

## 7. Recommended Approach

### Option A: Skills Only (Current - Recommended for Pi)

Keep current setup:
- JuliusBrussee/caveman skills in `~/.agents/skills/`
- Pi settings: `"skills": ["~/.agents/skills"]`
- Commands: `/caveman`, `/ultracave`, `/megacave`, `/caveman-compress`

**Best for**: Simple caveman voice in Pi. No extra dependencies.

### Option B: CLI for Other Agents + Skills for Pi

Use both:
- Caveman CLI for other agents (Claude, Codex, etc.)
- Skills for Pi

**Best for**: Multi-agent workflow. Full caveman features for supported agents, voice-only for Pi.

### Option C: Try CLI Wrap for Pi (Experimental)

Attempt to configure caveman CLI to work with Pi:

```bash
# 1. Install CLI
npm install -g @caveman-ai/cli

# 2. Update Pi
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

# 3. Try wrapping (may not work)
caveman pi

# 4. If fails, use manual proxy setup
caveman start --agent pi
```

**Best for**: Advanced users willing to debug. Unofficial support.

## 8. Comparison Matrix

| Feature | Skills | CLI |
|---------|--------|-----|
| Caveman voice | ✅ | ✅ |
| Input compression | ❌ | ✅ |
| Output compression | ✅ | ✅ |
| Auto mode | ❌ | ✅ |
| Blocks | ❌ | ✅ |
| Metering | ❌ | ✅ |
| Dashboard | ❌ | ✅ |
| Token analysis | ❌ | ✅ |
| Web compression | ❌ | ✅ |
| Pi support | ✅ | ❌ (OMP only) |
| Dependencies | None | Node.js 22.13+, Go binaries |
| Installation | Simple | Complex |

## 9. Verification

After any approach, verify:

```bash
# Check caveman status
/caveman status

# Test compression
/caveman
Test message
/stop caveman

# For CLI: check setup
caveman setup
```

## 10. Conclusion

**For Pi users**: Stick with skills approach. Simple, native, works.

**For multi-agent users**: Use CLI for supported agents + skills for Pi.

**For advanced users**: Experiment with CLI wrap for Pi, but expect to debug.

Current setup (skills only) is sufficient for caveman voice in Pi. CLI adds value for other agents and advanced features, but requires more setup and isn't officially supported for Pi.

## Source

- [JuliusBrussee/caveman CLI](https://github.com/JuliusBrussee/caveman)
- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
