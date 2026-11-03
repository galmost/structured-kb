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

## Source

- [freriadoc/Avalon — README and install.sh](https://github.com/freriadoc/Avalon)
- [Model: freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF (Hugging Face)](https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF)
- [ROCm install — package manager (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html)
- [ROCm system requirements — Debian 13 Instinct only; Radeon on Ubuntu/RHEL (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)
- [repo.radeon.com/rocm/apt/7.2.4/dists — only jammy and noble suites](https://repo.radeon.com/rocm/apt/7.2.4/dists/)
- [Debian Wiki — AtiHowTo](https://wiki.debian.org/AtiHowTo)
