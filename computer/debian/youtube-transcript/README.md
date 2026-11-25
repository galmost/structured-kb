# YouTube transcript extraction (Debian 13)

Pull the captions/transcript of a YouTube video without a browser or API key.

## Why yt-dlp

The plain caption endpoints are not reliably reachable from a shell or a
read-only web fetcher:

- `https://www.youtube.com/api/timedtext?v=<id>&lang=en...` returns HTTP 200
  with an **empty body** — YouTube now requires a PoToken (proof-of-origin)
  for most clients.
- The signed `baseUrl` found in the watch page's `ytInitialPlayerResponse`
  (`captionTracks`) has the same problem from curl.
- Web-fetch tools (`open_url`) are blocked on `youtube.com/api/timedtext`.

`yt-dlp` negotiates a working player client itself, so `--write-auto-subs`
just works. Install it ephemerally with `uv` (no system package needed):

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
- `--write-auto-subs`: include auto-generated (ASR) captions — most videos
  have no manual transcript. Drop it to get manual captions only.
- `--sub-format json3`: easiest to parse (events with `tStartMs` + `segs`).
  Other options: `srt`, `vtt`, `ttml`.
- Output: `video.en.json3` (also `.en.vtt` etc. if requested).

Check which caption tracks exist (watch page HTML, no login needed):

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

- ASR captions garble names: "Quen" = Qwen, "Orca Router" = mradermacher,
  "coder 3101" = coder3101, "Gemma 4E4B" = gemma-4-E4B, "Gemma 431B" =
  gemma-4-31B. Cross-check model/author names on Hugging Face before using
  them in configs.
- Auto captions have no punctuation and merge words occasionally; fine for
  summarising, quote-check against the audio for exact wording.
- Some videos have no caption track at all (then yt-dlp reports none).

## Example

`https://www.youtube.com/watch?v=j-VqPVjztJE` ("I Tested Every Uncensored
Local AI Model (8GB to 32GB VRAM)", Kai, 29:38): only an `en` ASR track
exists. Fetched 438 KB json3 → 793 segments → ~29k chars of text in seconds.

## Source

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — subtitle options
  (`--write-auto-subs`, `--sub-format`)
- YouTube `ytInitialPlayerResponse.captionTracks` structure
