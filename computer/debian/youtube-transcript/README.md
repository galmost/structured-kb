# YouTube transcript extraction (Debian 13)

Get YouTube video captions/transcript. No browser. No API key.

## Why yt-dlp

Plain caption endpoints not work from shell or web fetcher:

- `https://www.youtube.com/api/timedtext?v=<id>&lang=en...` returns HTTP 200 **empty body** — YouTube need PoToken (proof-of-origin) for most clients.
- Signed `baseUrl` in watch page `ytInitialPlayerResponse` (`captionTracks`) same problem from curl.
- Web-fetch tools (`open_url`) blocked on `youtube.com/api/timedtext`.

`yt-dlp` find working player itself, so `--write-auto-subs` work. Install with `uv` (no system package):

```bash
~/.local/bin/uv tool run yt-dlp --version   # 2026.10.26
```

## 1. Download the captions

```bash
cd /tmp
~/.local/bin/uv tool run yt-dlp --skip-download --write-auto-subs --write-subs \
  --sub-lang en --sub-format json3 \
  -o 'video.%(ext)s' 'https://www.youtube.com/watch?v=j-VqPVjztJE'
```

- `--skip-download`: captions only, no video.
- `--write-auto-subs`: get auto captions (ASR) — most videos no manual transcript. Drop for manual only.
- `--sub-format json3`: easy parse (`tStartMs` + `segs`). Others: `srt`, `vtt`, `ttml`.
- Output: `video.en.json3` (also `.en.vtt` etc.)

Check caption tracks exist (watch page HTML, no login):

```bash
curl -fsS -A 'Mozilla/5.0' 'https://www.youtube.com/watch?v=<id>&hl=en' -o /tmp/yt.html
# parse "captionTracks":[...] from ytInitialPlayerResponse -> languageCode, kind (asr), name
```

## 2. Convert json3 to a readable transcript

```bash
python3 - <<'EOF'
import json, re, html
d = json.load(open('/tmp/video.en.json3'))
lines = []
for e in d.get('events', []):
    if 'segs' not in e: continue
    t = e.get('tStartMs', 0) / 1000
    txt = ''.join(html.unescape(s.get('utf8','')) for s in e['segs'])
    txt = txt.replace('\n', ' ').strip()
    if not txt: continue
    m, s = divmod(int(t), 60); h, m = divmod(m, 60)
    ts = f'{h:02d}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'
    lines.append(f'[{ts}] {txt}')
open('/tmp/transcript.txt', 'w').write('\n'.join(lines))
plain = re.sub(r'\s+', ' ', ' '.join(l.split('] ', 1)[1] for l in lines))
open('/tmp/transcript_plain.txt', 'w').write(plain)
EOF
```

## Caveats

- ASR garble names: "Quen" = Qwen, "Orca Router" = mradermacher, "coder 3101" = coder3101, "Gemma 4E4B" = gemma-4-E4B, "Gemma 431B" = gemma-4-31B. Check model/author names on Hugging Face before use in configs.
- Auto captions no punctuation, merge words sometimes; OK for summary, check audio for exact words.
- Some videos no caption track (yt-dlp report none).

## Example

`https://www.youtube.com/watch?v=j-VqPVjztJE` ("I Tested Every Uncensored Local AI Model (8GB to 32GB VRAM)", Kai, 29:38): only `en` ASR track. Got 438 KB json3 → 793 segments → ~29k chars in seconds.

## Source

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — subtitle options (`--write-auto-subs`, `--sub-format`)
- YouTube `ytInitialPlayerResponse.captionTracks` structure