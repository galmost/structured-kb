# Avalon Setup (Debian 13 "trixie")

[Avalon](https://github.com/freriadoc/Avalon) is a llama.cpp fork tuned for
[Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) (125B MoE, ~89 GiB
GGUF) on one AMD RDNA3/RDNA4 GPU under ROCm 7. Its installer builds `llama-server` for
your GPU, downloads and SHA-256-verifies the model, and installs an `avalon-server`
launcher serving an OpenAI-compatible API on `http://127.0.0.1:8080`.

Debian caveat: AMD supports ROCm on Debian 13 only on Instinct GPUs; Radeon is
officially supported on Ubuntu 24.04/22.04 and RHEL. AMD's apt repo ships only `jammy`
and `noble` suites, so on trixie we register `noble` — it works because trixie's glibc
(2.41) is newer than noble's (2.39). Debian's own ROCm (5.7.1 in trixie) is too old;
the installer requires ROCm 7.x.

## 1. Prerequisites

The installer checks all of these and stops on failure:

- Debian 13 (trixie), x86_64, CPU with AVX2.
- AMD RDNA3/RDNA4 discrete GPU. `AMDGPU_TARGETS` mapping:

| card | gfx target |
|---|---|
| RX 7900 XT / XTX / GRE, PRO W7900 / W7800 | gfx1100 (measured target) |
| RX 7800 XT, RX 7700 XT | gfx1101 |
| RX 7600 | gfx1102 |
| RX 9070 series | gfx1201 |
| RX 9060 series | gfx1200 |

Detect yours after ROCm is installed:
`sg render -c '/opt/rocm/bin/rocminfo | grep -oE "\bgfx[0-9a-f]+\b" | sort -u'`.

- 20 GB VRAM for the full 256k context with MTP; below that run `-c 65536` (section 4).
- 16 GB RAM or more (hard fail below 14 GiB), ~98 GiB free disk for the model.

## 2. GPU driver, firmware, ROCm 7.2, build tools

```bash
pkexec apt update
pkexec apt install firmware-amd-graphics
pkexec /usr/sbin/usermod -aG video,render "$USER"   # re-login, or use: sg render -c '...'

pkexec mkdir --parents --mode=0755 /etc/apt/keyrings
curl -fsSL https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor | pkexec tee /etc/apt/keyrings/rocm.gpg > /dev/null
pkexec tee /etc/apt/sources.list.d/rocm.list << 'EOF'
deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/7.2.4 noble main
EOF
pkexec tee /etc/apt/preferences.d/rocm-pin-600 << 'EOF'
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 600
EOF
pkexec apt update
pkexec apt install rocm          # full meta package: amdclang++, rocminfo, rocBLAS...
pkexec apt install git cmake build-essential python3 python3-venv curl ca-certificates gnupg
```

Verify:

```bash
cat /opt/rocm/.info/version      # must start with 7.
sg render -c '/opt/rocm/bin/rocminfo | grep -oE "\bgfx[0-9a-f]+\b" | sort -u'
id                               # must list video and render
ls -l /dev/kfd /dev/dri/renderD* # both must exist
```

Verified on trixie: `noble` suite installed cleanly, 260 packages, no conflicts.

## 3. Run the installer

One command — checks the machine, clones to `~/Avalon`, builds `llama-server` for the
detected GPU (10–30 min), downloads the model with its MTP draft head (~89 GiB,
resumable), verifies every file's SHA-256, writes `~/.local/bin/avalon-server`:

```bash
AMDGPU_TARGETS=gfx1101 curl -fsSL https://raw.githubusercontent.com/freriadoc/Avalon/main/install.sh | bash
```

(`AMDGPU_TARGETS` optional; omit to auto-detect.) Knobs: `SKIP_MODEL=1` build only,
`MODEL_DIR` / `AVALON_DIR` / `BIN_DIR` relocate, `JOBS` build parallelism, `FORCE=1`
continue past a failed check.

## 4. Run and verify

```bash
avalon-server -c 65536     # -c 65536 on a 16 GB card (RX 7800 XT); omit for 20+ GB
curl -fsS http://127.0.0.1:8080/v1/models
curl -fsS -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf","messages":[{"role":"user","content":"Reply with exactly: pong"}],"max_tokens":64}'
```

Not re-logged into the `render` group yet? Prefix with `sg render -c '...'`, e.g.
`sg render -c 'avalon-server -c 65536'`. `HOST` / `PORT` env vars override the bind.

Verified on RX 7800 XT (gfx1101, 16 GB VRAM, `-c 65536`): model (88.3 GiB) loads,
server listens on `http://127.0.0.1:8080`, the request above returns `"content": "pong"`
at ~31 tokens/s, MTP draft acceptance 0.85 (17/20). The installer prints
`gfx1101: should work, not measured` — it works.

## 5. Add the Qwen2.5-Coder-7B variant (port 8081)

Second, smaller model: [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF)
q4_k_m GGUF, 2 shards, ~4.7 GiB. Served on `http://127.0.0.1:8081` as Vibe provider
`qwen-coder` (alias `qwen2.5-coder`). RAM fits only one server at a time, so the two
systemd user units conflict: starting one stops the other.

### 5.1 Download (resumable, SHA-256-verified)

```bash
mkdir -p ~/Avalon-models/Qwen2.5-Coder-7B-Instruct-GGUF
cat > /tmp/avalon-dl.txt << 'EOF'
https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf
  out=qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf
  checksum=sha-256=89f120544682078148c5a86117de9af3a65c339111262f2d3ff01d80d48b14be
https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m-00002-of-00002.gguf
  out=qwen2.5-coder-7b-instruct-q4_k_m-00002-of-00002.gguf
  checksum=sha-256=0183b3c850cfa96c31082c3af0123115300d3f62798c4448fa8f57bd0eac05e0
EOF
aria2c -c -x 16 -s 16 -k 1M --max-tries=0 --retry-wait=10 \
  -i /tmp/avalon-dl.txt -d ~/Avalon-models/Qwen2.5-Coder-7B-Instruct-GGUF \
  --log=/tmp/aria2-dl.log --log-level=info
```

`checksum=` lines make aria2 verify SHA-256 on completion and fail the file on
mismatch; `-c` resumes partial files via their `.aria2` control files. Expected sizes:
3993201376 and 689872288 bytes. Verify:

```bash
cd ~/Avalon-models/Qwen2.5-Coder-7B-Instruct-GGUF && sha256sum *.gguf
# 89f120544682078148c5a86117de9af3a65c339111262f2d3ff01d80d48b14be  qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf
# 0183b3c850cfa96c31082c3af0123115300d3f62798c4448fa8f57bd0eac05e0  qwen2.5-coder-7b-instruct-q4_k_m-00002-of-00002.gguf
ls   # no *.aria2 files remain once complete
```

### 5.2 Launcher

`~/.local/bin/qwen-coder-server` (chmod +x), mirrors `avalon-server`:

```bash
#!/usr/bin/env bash
# Qwen2.5-Coder-7B-Instruct (q4_k_m GGUF), OpenAI-compatible API on http://${HOST:-127.0.0.1}:${PORT:-8081}
# Extra arguments go to llama-server (e.g. -c 8192 for a smaller context).
cd "/home/galmost/Avalon-models/Qwen2.5-Coder-7B-Instruct-GGUF"
exec "/home/galmost/Avalon/build/bin/llama-server" -m qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf \
  -c "${CTX:-32768}" -b 4096 -ub 4096 -fa on --jinja --parallel 1 -ngl auto \
  --host "${HOST:-127.0.0.1}" --port "${PORT:-8081}" "$@"
```

### 5.3 Vibe config (`~/.vibe/config.toml`)

```toml
providers = [
    { name = "avalon", api_base = "http://127.0.0.1:8080/v1", api_key_env_var = "" },
    { name = "qwen-coder", api_base = "http://127.0.0.1:8081/v1", api_key_env_var = "" },
]

[[models]]
name = "Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf"
provider = "avalon"
alias = "avalon"
thinking = "low"
thinking_levels = [
    "low",
    "medium",
    "xhigh",
]
auto_compact_threshold = 60000

[[models]]
name = "qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf"
provider = "qwen-coder"
alias = "qwen2.5-coder"
thinking = "medium"
thinking_levels = [
    "low",
    "medium",
    "xhigh",
]
auto_compact_threshold = 24000
```

Two separate entries, one per local server: `thinking = "low"` for
`avalon` (Qwen3.8-Flash-Next, port 8080), `thinking = "medium"` for
`qwen2.5-coder` (port 8081). Both entries expose `thinking_levels` of
`low`, `medium`, `xhigh` — the only values the `--jinja` chat templates
accept; anything else (e.g. `high`, `max`) makes llama-server fail with a
Jinja `Unexpected reasoning effort` exception. Keep
`auto_compact_threshold` below the server context: 60000 for avalon
(`-c 65536`), 24000 for qwen2.5-coder (`-c 32768`, see 5.2) — otherwise
Vibe sends requests larger than the context and gets
`400 ... exceeds the available context size`.

### 5.4 systemd user services (start/stop individually)

`~/.config/systemd/user/qwen-coder.service`:

```ini
[Unit]
Description=Qwen2.5-Coder-7B llama-server (port 8081)
After=network.target
Conflicts=avalon.service

[Service]
Type=simple
ExecStart=/home/galmost/.local/bin/qwen-coder-server
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Add `Conflicts=qwen-coder.service` to the `[Unit]` of `~/.config/systemd/user/avalon.service`.
`qwen-coder.service` stays disabled (avalon is the boot default); RAM fits only one, and
`Conflicts` makes `start` of one stop the other:

```bash
systemctl --user daemon-reload
systemctl --user start qwen-coder.service   # stops avalon, serves :8081
systemctl --user start avalon.service       # stops qwen-coder, back to :8080
systemctl --user stop qwen-coder.service
systemctl --user status avalon.service qwen-coder.service
journalctl --user -u qwen-coder.service -f
```

Then select the model in Vibe: `vibe --model qwen2.5-coder`. Smoke test:
`curl -fsS http://127.0.0.1:8081/v1/models`.

## Troubleshooting

- `ROCm 5.7.1 found; Avalon is tested with ROCm 7.2.4 only` — you have Debian's ROCm.
  Remove it (`pkexec apt remove rocm-* hipcc rocminfo`) and install from
  `repo.radeon.com` (section 2). `FORCE=1` skips the check; not recommended.
- `no RDNA3 / RDNA4 discrete GPU found` — install `firmware-amd-graphics`, reboot,
  check `id` lists `video`/`render`, `/dev/kfd` exists, `dmesg | grep -i amdgpu` clean.
- `python3 -m venv failed` — `pkexec apt install python3-venv` (trixie: pulls
  `python3.13-venv`).
- Less than 20 GB VRAM — start with `avalon-server -c 65536`.
- Less than 14 GiB RAM or 98 GiB free disk — installer refuses. Point `MODEL_DIR` at a
  bigger disk; RAM cannot be worked around.
- `avalon-server: command not found` — add `export PATH="$HOME/.local/bin:$PATH"` to
  `~/.bashrc`, re-login.
- `SHA-256 mismatch` — rerun the installer; downloads resume, verified files skip.
- `model (88.3 GiB) is larger than RAM: prompt cache disabled` — benign on 32 GB RAM
  (model is memory-mapped). Add `--cache-ram N` to force a prompt cache.
- Slow model download (~4–15 MB/s, Hugging Face caps per-IP bandwidth; full run took
  ~2.5 h) — rerun the installer to resume. See `computer/debian/aria2c` for segmented
  parallel downloads of other large files.
- Qwen shard partial / `*.aria2` file remains — rerun the `aria2c -c -i /tmp/avalon-dl.txt ...`
  command from 5.1; it resumes from the control file. SHA-256 mismatch after completion —
  delete the file and its `.aria2`, rerun; do not rename a failed file into place.
- `Conflicts` did not stop the other server / port busy — check `ss -tlnp | grep -E ':8080|:8081'`;
  if a server was started manually (not via systemd) stop it by PID first.
- Vibe session restore fails with `tagged-union[RustAcceptedApplyResult,RustRejectedApplyResult]`
  and `runtime_builtin.arguments ... Input should be an object [type=dict_type, input_type=str]` —
  a recorded tool call with `arguments` as a bare string (e.g. `'aria2c -i /tmp/avalon-dl... ... 2>&1'`)
  poisons that session's replay in `~/.vibe/logs/vibe.log`. That session cannot be resumed;
  start a fresh session and rerun the command with proper object arguments.
- Vibe + `qwen2.5-coder` returns `400 ... request (N tokens) exceeds the available context size (32768 tokens)`
  — the conversation outgrew the server's `-c 32768`. Set `auto_compact_threshold = 24000`
  on the `qwen2.5-coder` model entry (section 5.3), or start the server with a larger
  `CTX` (section 5.2).
- Vibe + `qwen2.5-coder` logs `Completion neither reasoned nor called a tool ... tools_offered=12 finish_reason=stop`
  and only answers in text — the 7B model is offered all tools but does not emit tool
  calls. Not a permissions problem; use it for text-only work (e.g. caveman-compress,
  `[utility_models]`) and use `avalon` or a hosted model for file/repo agent tasks.
- Vibe + local model fails with `Jinja Exception: Unexpected reasoning effort ... Supported types are xhigh (default), medium, and low`
  — the model entry has a `thinking` value outside `low`/`medium`/`xhigh` (e.g. `high`,
  `max`). Fix the entry per section 5.3.

## Source

- [freriadoc/Avalon — README and install.sh](https://github.com/freriadoc/Avalon)
- [Model: freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF (Hugging Face)](https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF)
- [ROCm install — package manager (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html)
- [ROCm system requirements — Debian 13 Instinct only; Radeon on Ubuntu/RHEL (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)
- [repo.radeon.com/rocm/apt/7.2.4/dists — only jammy and noble suites](https://repo.radeon.com/rocm/apt/7.2.4/dists/)
- [Debian Wiki — AtiHowTo](https://wiki.debian.org/AtiHowTo)
- [Model: Qwen/Qwen2.5-Coder-7B-Instruct-GGUF (Hugging Face)](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF)
