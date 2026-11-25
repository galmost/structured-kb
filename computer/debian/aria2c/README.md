# aria2c Setup (Debian 13)

`aria2c` lightweight tool. Downloads fast. Supports HTTP(S), FTP, SFTP, BitTorrent. Multi-connection. Resume. Use when curl, wget, `hf download` without `hf_transfer` too slow. Server caps speed per connection. Hugging Face does this.

## 1. Install

```bash
pkexec apt install -y aria2
```

Use `sudo apt install -y aria2` if no sudo password.

Verify:

```bash
aria2c --version
```

Debian 13 has aria2 1.37.0.

## 2. Single file, segmented download

```bash
aria2c -x 16 -s 16 -c https://example.com/bigfile.iso
```

- `-x 16` / `-s 16`: 16 connections, 16 segments. Server need range requests. Hugging Face has them.
- `-c`: resume interrupted download.
- Downloads to current dir. `-d <dir>` set other dir.

## 3. Download a list of URLs from an input file

Input file: one URL per line. More options on next lines (tab + `key=value`). `out=` set path relative to `--dir`. Keeps subdirectories:

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

- `-i <file>`: input file. `-j 16`: 16 downloads at once.
- `-c`: resume. Unfinished files keep `.aria2` file. Run same command to continue.
- `--file-allocation=none`: skip disk pre-allocate. Faster start. Needed on some filesystems.
- `--summary-interval=120`: print progress every 120 seconds.

Make input file for whole Hugging Face repo with HF API (skip thumbnails, docs):

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

Do not use `pgrep -f aria2c` to check alive. It matches shell command too. Use `pgrep -x aria2c`.

Done when target dir has expected size and no `*.aria2` files remain:

```bash
find /home/galmost/models/repo -name '*.aria2' | wc -l   # 0 means complete
```

## 5. Hugging Face notes

- HF caps bandwidth per IP (~11 MB/s seen). Raising `-j`/`-x` past ~16 no help. Cap is per IP.
- `hf download` single stream without `hf_transfer`. 3-4x slower than aria2c on HF. If installer placed complete files, `hf download --local-dir` skips files with matching size. Mixing both safe.
- Interrupted aria2 files: `hf download` re-downloads from scratch unless size matches. Finish with aria2 first.

## Troubleshooting

### Download stalls at 0 B/s or "resource unavailable"
Server reject too many connections. Lower `-x`/`-s`:

```bash
aria2c -x 4 -s 4 -c <url>
```

### Resume does not work / file restarts
`.aria2` file deleted or server ignore range requests (`--allow-overwrite=true` then redownload). Keep control files until done. Check server support:

```bash
curl -sI https://example.com/bigfile.iso | grep -i accept-ranges
```

### `out=` subdirectory not created
aria2 makes parent dirs for `out=` auto. If fail, make first: `mkdir -p <dir>/MTP`.

## Source

- aria2 man page and docs: https://aria2.github.io/manual/en/html/aria2c.html
- Hugging Face `hf` CLI: https://huggingface.co/docs/huggingface_hub/en/guides/cli