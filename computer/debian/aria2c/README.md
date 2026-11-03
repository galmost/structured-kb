# aria2c Setup (Debian 13)

`aria2c` is a lightweight command-line download utility that supports
HTTP(S), FTP, SFTP and BitTorrent, with multi-connection (segmented)
downloads and resume. Use it when a single-stream download (curl, wget,
`hf download` without `hf_transfer`) is slower than your link because the
server caps per-connection rate — common with Hugging Face, which limits
per-IP throughput.

## 1. Install

```bash
pkexec apt install -y aria2
```

Use `sudo apt install -y aria2` instead if passwordless sudo is configured.

Verify:

```bash
aria2c --version
```

Debian 13 (trixie) ships aria2 1.37.0.

## 2. Single file, segmented download

```bash
aria2c -x 16 -s 16 -c https://example.com/bigfile.iso
```

- `-x 16` / `-s 16`: up to 16 connections, 16 segments per file. The server
  must support range requests; Hugging Face does.
- `-c`: continue/resume if a previous download was interrupted.
- Downloads to the current directory by default; `-d <dir>` sets the target.

## 3. Download a list of URLs from an input file

aria2 input files have one URL per line, with optional per-URL directives on
following lines (one tab-indented `key=value` per line). `out=` sets the
output path relative to `--dir`, and preserves subdirectories:

```bash
cat > /tmp/files.txt <<'EOF'
https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF/resolve/main/model-00001-of-00033.gguf
	out=model-00001-of-00033.gguf
https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF/resolve/main/MTP/mtp-model.gguf
	out=MTP/mtp-model.gguf
EOF

aria2c -i /tmp/files.txt -j 16 -x 16 -s 16 -c \
  --allow-overwrite=true --file-allocation=none \
  --dir=/home/galmost/models/Qwen3.8-Flash-Next-Avalon-GGUF \
  --summary-interval=120 | tee /tmp/aria2c.log
```

- `-i <file>`: input file. `-j 16`: 16 downloads in parallel.
- `-c`: resume. Incomplete files keep an `.aria2` control file next to them;
  rerunning the same command resumes instead of restarting.
- `--file-allocation=none`: skip pre-allocating disk (faster start, needed
  on some filesystems).
- `--summary-interval=120`: print a progress summary every 120 seconds.

Generate the input file for a whole Hugging Face repo with the HF API
(skip thumbnails and docs):

```bash
curl -fsSL 'https://huggingface.co/api/models/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF' \
  | python3 -c 'import json,sys; [print(f"https://huggingface.co/freriadoc/Qwen3.8-Flash-Next-Avalon-GGUF/resolve/main/{s}") or print(f"\tout={s}") for s in json.load(sys.stdin)["siblings"] if not s["rfilename"].endswith((".jpg", ".md"))]' \
  > /tmp/avalon-files.txt
```

## 4. Run in the background and monitor

```bash
nohup aria2c -i /tmp/files.txt -j 16 -x 16 -s 16 -c \
  --dir=/home/galmost/models/repo --summary-interval=120 \
  > /tmp/aria2c.log 2>&1 &
pgrep -x aria2c   # prints a PID while running; no output when done
du -sh /home/galmost/models/repo
```

Do not use `pgrep -f aria2c` to check liveness — it also matches the shell
command that contains the string. Use `pgrep -x aria2c`.

Done when the target directory reaches the expected total size and no
`*.aria2` control files remain:

```bash
find /home/galmost/models/repo -name '*.aria2' | wc -l   # 0 means complete
```

## 5. Hugging Face notes

- HF caps aggregate per-IP bandwidth (observed ~11 MB/s on a much faster
  link). Raising `-j`/`-x` beyond ~16 does not help; the cap is per IP, not
  per connection.
- `hf download` (used by many installers) is single-stream without
  `hf_transfer` and can be 3-4x slower than aria2c against HF. If an installer
  already placed complete files in its model dir, `hf download --local-dir`
  skips files whose size matches the remote, so mixing both is safe.
- Interrupted aria2 files are re-downloaded from scratch by `hf download`
  unless the size matches; complete them with aria2 first.

## Troubleshooting

### Download stalls at 0 B/s or "resource unavailable"
The server may reject too many connections. Lower `-x`/`-s`:

```bash
aria2c -x 4 -s 4 -c <url>
```

### Resume does not work / file restarts
The `.aria2` control file was deleted, or the server ignores range requests
(`--allow-overwrite=true` then redownloads). Keep control files until the
download finishes; check server support with:

```bash
curl -sI https://example.com/bigfile.iso | grep -i accept-ranges
```

### `out=` subdirectory not created
aria2 creates parent directories for `out=` paths automatically; if it
fails, create them first: `mkdir -p <dir>/MTP`.

## Source

- aria2 man page and docs: https://aria2.github.io/manual/en/html/aria2c.html
- Hugging Face `hf` CLI: https://huggingface.co/docs/huggingface_hub/en/guides/cli
