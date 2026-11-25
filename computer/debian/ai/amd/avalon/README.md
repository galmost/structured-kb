# Avalon Setup (Debian 13 "trixie")

[Avalon](https://github.com/freriadoc/Avalon) be llama.cpp fork. Tuned for [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) (125B MoE, ~89 GiB GGUF) on one AMD RDNA3/RDNA4 GPU under ROCm 7. Installer build `llama-server` for your GPU, download and SHA-256-verify model, install `avalon-server` launcher. Serve OpenAI-compatible API on `http://127.0.0.1:8080`.

Debian caveat: AMD support ROCm on Debian 13 only on Instinct GPUs. Radeon officially supported on Ubuntu 24.04/22.04 and RHEL. AMD apt repo ship only `jammy` and `noble` suites. On trixie register `noble` — work because trixie glibc (2.41) newer than noble (2.39). Debian own ROCm (5.7.1 in trixie) too old. Installer require ROCm 7.x.

## 1. Prerequisites

Installer check all these. Stop on failure:

- Debian 13 (trixie), x86_64, CPU with AVX2.
- AMD RDNA3/RDNA4 discrete GPU. `AMDGPU_TARGETS` mapping:

| card | gfx target |
|---|---|
| RX 7900 XT / XTX / GRE, PRO W7900 / W7800 | gfx1100 (measured target) |
| RX 7800 XT, RX 7700 XT | gfx1101 |
| RX 7600 | gfx1102 |
| RX 9070 series | gfx1201 |
| RX 9060 series | gfx1200 |

Detect yours after ROCm installed:
`sg render -c '/opt/rocm/bin/rocminfo | grep -oE "\bgfx[0-9a-f]+\b" | sort -u'`.

- 20 GB VRAM for full 256k context with MTP. Below that run `-c 65536` (section 4).
- 16 GB RAM or more (hard fail below 14 GiB), ~98 GiB free disk for model.

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

Verified on trixie: `noble` suite install cleanly, 260 packages, no conflicts.

## 3. Run the installer

One command — check machine, clone to `~/Avalon`, build `llama-server` for detected GPU (10–30 min), download model with MTP draft head (~89 GiB, resumable), verify every file SHA-256, write `~/.local/bin/avalon-server`:

```bash
AMDGPU_TARGETS=gfx1101 curl -fsSL https://raw.githubusercontent.com/freriadoc/Avalon/main/install.sh | bash
```

(`AMDGPU_TARGETS` optional. Omit to auto-detect.) Knobs: `SKIP_MODEL=1` build only, `MODEL_DIR` / `AVALON_DIR` / `BIN_DIR` relocate, `JOBS` build parallelism, `FORCE=1` continue past failed check.

## 4. Run and verify

```bash
avalon-server -c 65536     # -c 65536 on a 16 GB card (RX 7800 XT); omit for 20+ GB
curl -fsS http://127.0.0.1:8080/v1/models
curl -fsS -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf","messages":[{"role":"user","content":"Reply with exactly: pong"}],"max_tokens":64}'
```

Not re-logged into `render` group yet? Prefix with `sg render -c '...'`, e.g. `sg render -c 'avalon-server -c 65536'`. `HOST` / `PORT` env vars override bind.

Verified on RX 7800 XT (gfx1101, 16 GB VRAM, `-c 65536`): model (88.3 GiB) load, server listen on `http://127.0.0.1:8080`, request above return `"content": "pong"` at ~31 tokens/s, MTP draft acceptance 0.85 (17/20). Installer print `gfx1101: should work, not measured` — it work.

## 5. Add the Qwen2.5-Coder-7B variant (port 8081)

Second, smaller model: [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF) q4_k_m GGUF, 2 shards, ~4.7 GiB. Serve on `http://127.0.0.1:8081` as Vibe provider `qwen-coder` (alias `qwen2.5-coder`). RAM fit only one server at a time. Two systemd user units conflict: start one stop other.

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

`checksum=` lines make aria2 verify SHA-256 on completion and fail file on mismatch. `-c` resume partial files via `.aria2` control files. Expected sizes: 3993201376 and 689872288 bytes. Verify:

```bash
cd ~/Avalon-models/Qwen2.5-Coder-7B-Instruct-GGUF && sha256sum *.gguf
# 89f120544682078148c5a86117de9af3a65c339111262f2d3ff01d80d48b14be  qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf
# 0183b3c850cfa96c31082c3af0123115300d3f62798c4448fa8f57bd0eac05e0  qwen2.5-coder-7b-instruct-q4_k_m-00002-of-00002.gguf
ls   # no *.aria2 files remain once complete
```

### 5.2 Launcher

`~/.local/bin/qwen-coder-server` (chmod +x), mirror `avalon-server`:

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

Two separate entries, one per local server: `thinking = "low"` for `avalon` (Qwen3.8-Flash-Next, port 8080), `thinking = "medium"` for `qwen2.5-coder` (port 8081). Both entries expose `thinking_levels` of `low`, `medium`, `xhigh` — only values the `--jinja` chat templates accept. Anything else (e.g. `high`, `max`) make llama-server fail with Jinja `Unexpected reasoning effort` exception. Keep `auto_compact_threshold` below server context: 60000 for avalon (`-c 65536`), 24000 for qwen2.5-coder (`-c 32768`, see 5.2) — otherwise Vibe send requests larger than context and get `400 ... exceeds the available context size`.

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

Add `Conflicts=qwen-coder.service` to `[Unit]` of `~/.config/systemd/user/avalon.service`. `qwen-coder.service` stay disabled (avalon be boot default). RAM fit only one. `Conflicts` make `start` of one stop other:

```bash
systemctl --user daemon-reload
systemctl --user start qwen-coder.service   # stops avalon, serves :8081
systemctl --user start avalon.service       # stops qwen-coder, back to :8080
systemctl --user stop qwen-coder.service
systemctl --user status avalon.service qwen-coder.service
journalctl --user -u qwen-coder.service -f
```

Then select model in Vibe: `vibe --model qwen2.5-coder`. Smoke test: `curl -fsS http://127.0.0.1:8081/v1/models`.

## 6. Model recovery (models are not backed up)

`~/Avalon-models` be 134G — too big for off-box backup. Recovery be: restore home folder from gark_home git snapshots (configs, wrappers, server scripts), then re-download models and verify against manifest:

```bash
# manifest with sha256 per GGUF, committed in this folder:
cat models-manifest.sha256        # 39 files under ~/Avalon-models/<repo>/
# re-download (Hugging Face repos named after the folders, e.g.
#   freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF, Qwen/Qwen2.5-Coder-7B-Instruct-GGUF)
# or re-run the Avalon installer, which downloads and SHA-256-verifies itself:
avalon-server -c 65536            # after reinstall, first run fetches missing files
# verify:
cd ~/Avalon-models && sha256sum -c ~/git/structured-kb/computer/debian/ai/amd/avalon/models-manifest.sha256
```

If sha256 mismatch, delete that file and re-download. Do not serve model that fail verification.

## Troubleshooting

- `ROCm 5.7.1 found; Avalon is tested with ROCm 7.2.4 only` — you have Debian ROCm. Remove it (`pkexec apt remove rocm-* hipcc rocminfo`) and install from `repo.radeon.com` (section 2). `FORCE=1` skip check. Not recommended.
- `no RDNA3 / RDNA4 discrete GPU found` — install `firmware-amd-graphics`, reboot, check `id` list `video`/`render`, `/dev/kfd` exist, `dmesg | grep -i amdgpu` clean.
- `python3 -m venv failed` — `pkexec apt install python3-venv` (trixie: pull `python3.13-venv`).
- Less than 20 GB VRAM — start with `avalon-server -c 65536`.
- Less than 14 GiB RAM or 98 GiB free disk — installer refuse. Point `MODEL_DIR` at bigger disk. RAM cannot be worked around.
- `avalon-server: command not found` — add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc`, re-login.
- `SHA-256 mismatch` — rerun installer. Downloads resume, verified files skip.
- `model (88.3 GiB) is larger than RAM: prompt cache disabled` — benign on 32 GB RAM (model memory-mapped). Add `--cache-ram N` to force prompt cache.
- Slow model download (~4–15 MB/s, Hugging Face cap per-IP bandwidth. Full run took ~2.5 h) — rerun installer to resume. See `computer/debian/aria2c` for segmented parallel downloads of other large files.
- Qwen shard partial / `*.aria2` file remain — rerun `aria2c -c -i /tmp/avalon-dl.txt ...` command from 5.1. It resume from control file. SHA-256 mismatch after completion — delete file and its `.aria2`, rerun. Do not rename failed file into place.
- `Conflicts` did not stop other server / port busy — check `ss -tlnp | grep -E ':8080|:8081'`. If server started manually (not via systemd) stop it by PID first.
- Vibe session restore fail with `tagged-union[RustAcceptedApplyResult,RustRejectedApplyResult]` and `runtime_builtin.arguments ... Input should be an object [type=dict_type, input_type=str]` — recorded tool call with `arguments` as bare string (e.g. `'aria2c -i /tmp/avalon-dl... ... 2>&1'`) poison that session replay in `~/.vibe/logs/vibe.log`. That session cannot be resumed. Start fresh session and rerun command with proper object arguments.
- Vibe + `qwen2.5-coder` return `400 ... request (N tokens) exceeds the available context size (32768 tokens)` — conversation outgrew server `-c 32768`. Set `auto_compact_threshold = 24000` on `qwen2.5-coder` model entry (section 5.3), or start server with larger `CTX` (section 5.2).
- Vibe + `qwen2.5-coder` log `Completion neither reasoned nor called a tool ... tools_offered=12 finish_reason=stop` and only answer in text — 7B model offered all tools but not emit tool calls. Not permissions problem. Use for text-only work (e.g. caveman-compress, `[utility_models]`). Use `avalon` or hosted model for file/repo agent tasks.
- Vibe + local model fail with `Jinja Exception: Unexpected reasoning effort ... Supported types are xhigh (default), medium, and low` — model entry have `thinking` value outside `low`/`medium`/`xhigh` (e.g. `high`, `max`). Fix entry per section 5.3.

## Source

- [freriadoc/Avalon — README and install.sh](https://github.com/freriadoc/Avalon)
- [Model: freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF (Hugging Face)](https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF)
- [ROCm install — package manager (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html)
- [ROCm system requirements — Debian 13 Instinct only; Radeon on Ubuntu/RHEL (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)
- [repo.radeon.com/rocm/apt/7.2.4/dists — only jammy and noble suites](https://repo.radeon.com/rocm/apt/7.2.4/dists/)
- [Debian Wiki — AtiHowTo](https://wiki.debian.org/AtiHowTo)
- [Model: Qwen/Qwen2.5-Coder-7B-Instruct-GGUF (Hugging Face)](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF)