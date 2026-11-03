# Avalon Setup (Debian 13 "trixie")

[Avalon](https://github.com/freriadoc/Avalon) is a fork of llama.cpp tuned for one
model, [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) (125B MoE,
~89 GiB GGUF), on one AMD RDNA3/RDNA4 GPU under ROCm 7 with the MoE experts in system
RAM. Its installer builds `llama-server` for your GPU, downloads and SHA-256-verifies
the model, and installs an `avalon-server` launcher serving an OpenAI-compatible API on
`http://127.0.0.1:8080`. This note covers Debian 13 (trixie) with ROCm 7.2.4.

Debian caveat, up front: AMD officially supports ROCm on Debian 13 only on Instinct
(MI300X/MI350X) GPUs; Radeon cards are officially supported on Ubuntu 24.04/22.04 and
RHEL only. The `repo.radeon.com` ROCm 7.2.4 apt repo ships only `jammy` and `noble`
suites, so on trixie we register the `noble` suite — this works because trixie's glibc
(2.41) is newer than noble's (2.39), and packages built against an older glibc run on
a newer one. Debian's own ROCm packages (5.7.1 in trixie) are too old: Avalon's
installer refuses anything but ROCm 7.x. If you want fully official support for a
Radeon card, use Ubuntu 24.04 instead.

## 1. Hardware and OS prerequisites

The installer checks all of these and stops on failure:

- Debian 13 (trixie), x86_64, CPU with **AVX2** (the CPU-side expert kernels need it).
- AMD **RDNA3** discrete GPU: RX 7900 XT / XTX / GRE (gfx1100, the measured target),
  RX 7800 XT / 7700 XT (gfx1101), RX 7600 (gfx1102). **RDNA4** (gfx1200 / gfx1201, e.g.
  RX 9060 / 9070) is reported working by a user, not measured. APUs and older
  generations are refused.
- **20 GB VRAM or more** for the full 256k context with MTP; below that, run with
  `-c 65536` (see Troubleshooting).
- **16 GB RAM or more** (the installer hard-fails below 14 GiB; the ~89 GiB model is
  memory-mapped, and what does not fit in RAM is re-read from disk).
- **~98 GiB free disk** where the model goes (default `~/Avalon-models/...`).
- Debian 13's stock 6.12 kernel already has the `amdgpu` driver for gfx1100; only the
  firmware package is missing (next section).

GPU target mapping for `AMDGPU_TARGETS` / `-DAMDGPU_TARGETS`:

| card | gfx target |
|---|---|
| RX 7900 XT / XTX / GRE, PRO W7900 / W7800 | gfx1100 |
| RX 7800 XT, RX 7700 XT / 7700 | gfx1101 |
| RX 7600 | gfx1102 |
| RX 9070 series | gfx1201 |
| RX 9060 series | gfx1200 |

Detect yours after ROCm is installed with
`/opt/rocm/bin/rocminfo | grep -oE '\bgfx[0-9a-f]+\b' | sort -u`.

## 2. GPU driver and firmware (Debian packages)

ROCm needs the `amdgpu` kernel module (in Debian's kernel) plus the card's firmware
and access to `/dev/kfd` and `/dev/dri/renderD128`. Enable `non-free-firmware` in
`/etc/apt/sources.list` if it is not there yet (the trixie installer adds it by
default), then:

```bash
pkexec apt update
pkexec apt install firmware-amd-graphics
pkexec /usr/sbin/usermod -aG video,render "$USER"   # then log out and back in
```

Until you re-login, current shells pick up the new group with
`sg render -c '<command>'` (or `sg video -c '...'`).

Verify after re-login:

```bash
id                                  # must list video and render
ls -l /dev/kfd /dev/dri/renderD*    # both must exist
dmesg | grep -i amdgpu | tail       # module loaded, no firmware errors
```

## 3. Install ROCm 7.2 from AMD's apt repo (noble suite on trixie)

Register AMD's repo using the `noble` suite, pin it, and install the `rocm` meta
package (several GB; it pulls in `amdclang`/`amdclang++` from `rocm-llvm`, `rocminfo`,
`rocm-device-libs`, rocBLAS and hipBLAS — ggml's HIP backend does
`find_package(hip/hipblas/rocblas REQUIRED)`, so a partial install fails at cmake
time):

```bash
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
pkexec apt install rocm
```

Check the version string the way the installer does, and see the detected GPU
(run via `sg render -c '...'` if you have not re-logged since adding the group):

```bash
cat /opt/rocm/.info/version                       # must start with 7.
sg render -c '/opt/rocm/bin/rocminfo | grep -oE "\bgfx[0-9a-f]+\b" | sort -u'
```

Verified on trixie: the `noble` suite installed cleanly — 260 packages from
`repo.radeon.com/rocm/apt/7.2.4`, no conflicts, `/opt/rocm/.info/version` = 7.2.4,
`rocminfo` reports gfx1101 on an RX 7800 XT.

Only the ROCm compute repo is added above; the separate `graphics/7.2.4/ubuntu` repo
in AMD's docs is for the graphics stack and is not needed for Avalon.

## 4. Build tools

The installer checks for `git`, `cmake` and `python3`; Debian also needs `python3-venv`
for the virtualenv it creates to download the model:

```bash
pkexec apt install git cmake build-essential python3 python3-venv curl wget ca-certificates gnupg
```

## 5. Run the installer

One command — it checks the machine, clones the repo to `~/Avalon`, builds
`llama-server` for the detected GPU (10–30 min), downloads the model with its MTP
draft head (~89 GiB, resumable), verifies every file's SHA-256 against Hugging Face,
and writes the `~/.local/bin/avalon-server` launcher:

```bash
curl -fsSL https://raw.githubusercontent.com/freriadoc/Avalon/main/install.sh | bash
```

Environment knobs (see the top of `install.sh`): `AMDGPU_TARGETS=gfx1100` to skip GPU
detection, `SKIP_MODEL=1` to build only, `MODEL_DIR` / `AVALON_DIR` / `BIN_DIR` to
relocate, `JOBS` for build parallelism, `FORCE=1` to continue past a failed check.

## 6. Run and verify

```bash
avalon-server        # OpenAI-compatible API on http://127.0.0.1:8080
curl http://127.0.0.1:8080/v1/models
```

On a 16 GB card (RX 7800 XT) use a smaller context — verified working:

```bash
sg render -c 'avalon-server -c 65536'   # if not re-logged into the render group
curl -fsS http://127.0.0.1:8080/v1/models
curl -fsS -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf","messages":[{"role":"user","content":"Reply with exactly: pong"}],"max_tokens":64}'
```

Verified output on an RX 7800 XT (gfx1101, 16 GB VRAM) with `-c 65536`: the model
(88.3 GiB) loads, the server listens on `http://127.0.0.1:8080`, and the request
above returns `"content": "pong"` at ~31 tokens/s with MTP draft acceptance 0.85
(17 of 20 drafted tokens accepted). The installer warns `gfx1101: should work, not
measured` — it does work.

Extra arguments are forwarded to `llama-server` (e.g. `avalon-server -c 65536`);
`HOST` and `PORT` override the bind address. The launcher runs the tuned command:
256k context, `-b 9536 -ub 9536 -fa on -ctk q8_0 -ctv q4_0 --jinja --parallel 1`,
plus the shared MTP draft head with `--spec-draft-n-max 2`.

## 7. Manual build (without the installer)

```bash
git clone https://github.com/freriadoc/Avalon && cd Avalon
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100 -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=/opt/rocm/bin/amdclang -DCMAKE_CXX_COMPILER=/opt/rocm/bin/amdclang++
cmake --build build -j"$(nproc)" --target llama-server
```

Download the model (33 parts + MTP head) with the `hf` CLI:

```bash
python3 -m venv .venv && .venv/bin/pip install -q "huggingface_hub>=0.34"
.venv/bin/hf download freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF --local-dir Qwen3.8-Flash-Next-Avalon-GGUF
```

Run:

```bash
cd Qwen3.8-Flash-Next-Avalon-GGUF
../Avalon/build/bin/llama-server -m Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf \
  -c 262144 -b 9536 -ub 9536 -fa on -ctk q8_0 -ctv q4_0 --jinja --parallel 1 \
  -md MTP/mtp-Qwen3.8-Flash-Next-shared-IQ3K-IQ4NL-FR65k.gguf --spec-type draft-mtp \
  --spec-draft-n-max 2 -ubd 256 -ctkd q8_0 -ctvd q8_0
```

## Troubleshooting

- `error: ROCm 5.7.1 found; Avalon is tested with ROCm 7.2.4 only` — you have Debian's
  own ROCm, not AMD's. Remove it (`pkexec apt remove hipcc rocminfo rocm-*`) and
  install from `repo.radeon.com` as in section 3. `FORCE=1` skips the check but is not
  recommended.
- `no RDNA3 / RDNA4 discrete GPU found (rocminfo reports: nothing)` — `/dev/kfd` is
  missing or you lack permission: install `firmware-amd-graphics`, reboot, make sure
  `id` lists `video` and `render`, check `dmesg | grep -i amdgpu` for firmware errors.
- apt reports unmet dependencies for the `noble` suite on trixie — usually fine
  because of glibc forward compatibility; install the full `rocm` meta package so the
  coherent set resolves together, then `pkexec apt install -f`. If apt still refuses,
  use Ubuntu 24.04 (officially supported for Radeon) instead of Debian.
- `python3 -m venv failed` — `pkexec apt install python3-venv` (on trixie this pulls
  `python3.13-venv`).
- `model (88.3 GiB) is larger than RAM (30.5 GiB): prompt cache disabled` — expected
  on 32 GB RAM; the model is memory-mapped, so this warning is benign. Add
  `--cache-ram N` to `avalon-server` if you want a prompt cache in RAM.
- Model download is slow (~4–15 MB/s; Hugging Face caps per-IP bandwidth) — the
  `hf download` run fetched all 37 files (~89 GiB) in about 2.5 h. It is resumable:
  rerun the installer and completed files are skipped. For other large downloads,
  see the `computer/debian/aria2c` note for segmented parallel downloads.
- Less than 20 GB VRAM: the 256k context with MTP may not fit — start with
  `avalon-server -c 65536`.
- Less than 14 GiB RAM or less than 98 GiB free: the installer refuses. Point
  `MODEL_DIR` at a bigger disk (`MODEL_DIR=/mnt/bigdisk/model curl ... | bash`); more
  RAM cannot be worked around (the model is memory-mapped).
- `avalon-server: command not found` — `~/.local/bin` is not in `PATH`; add
  `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` and re-login.
- `SHA-256 mismatch` during install — rerun the same installer command: downloads
  resume and verified files are skipped (`.avalon-verified` next to the model).
- NVIDIA GPU instead: the installer is ROCm-only, but the code builds with CUDA —
  `cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DCMAKE_BUILD_TYPE=Release`
  then `cmake --build build -j"$(nproc)" --target llama-server` (measured on an RTX 4090;
  kernels not tuned for NVIDIA yet).

## Source

- [freriadoc/Avalon — README and install.sh](https://github.com/freriadoc/Avalon)
- [Model: freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF (Hugging Face)](https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF)
- [ROCm install on Linux — package manager (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html)
- [ROCm system requirements — Debian 13 supported on Instinct only; Radeon on Ubuntu/RHEL (AMD docs)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)
- [repo.radeon.com/rocm/apt/7.2.4/dists — only jammy and noble suites exist](https://repo.radeon.com/rocm/apt/7.2.4/dists/)
- [Debian Wiki — AtiHowTo (firmware-amd-graphics, video/render groups)](https://wiki.debian.org/AtiHowTo)
