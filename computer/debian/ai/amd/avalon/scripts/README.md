# Avalon Call Stats Scripts (Debian 13 "trixie")

`avalon_stats.py` read `avalon.service` journal. Make per-call cost report. Show minutes per completed request. Split prompt-eval and gen time. Show mean, median, percentiles. Show prompt vs gen split. Use to find which calls dominate wall time and if call prompt-bound or gen-bound.

Stdlib only. Python 3.9+. No root. `avalon.service` is systemd *user* unit. `journalctl --user` read it.

## 1. Prerequisites

- `avalon.service` run as user unit (`~/.config/systemd/user/avalon.service`, see parent note `computer/debian/ai/amd/avalon`).
- `python3` (3.9+).
- Journal entries from `llama-server` at default level. Lines script needs look like this:

```
slot print_timing: id  0 | task 2851 | prompt eval time = 435601.21 ms / 40317 tokens (   92.51 token per second)
slot print_timing: id  0 | task 2851 |      eval time = 61000.00 ms / 905 tokens (   14.84 token per second)
slot print_timing: id  0 | task 2851 |     total time = 496601.21 ms / 41222 tokens
```

Each metric own line. Pass `-o short-iso` for one timestamp per line.

## 2. Run it

Current boot:

```bash
journalctl --user -u avalon.service --boot -o short-iso --no-pager | ./avalon_stats.py
```

Every boot in journal (more calls, but task ids repeat across launches — script keys on PID + task, so they stay separate):

```bash
journalctl --user -u avalon.service -o short-iso --no-pager | ./avalon_stats.py
```

Machine-readable output, for plotting or other tool:

```bash
journalctl --user -u avalon.service --boot -o short-iso --no-pager | ./avalon_stats.py --csv
```

Saved log file instead of live journal:

```bash
./avalon_stats.py server.log
```

## 3. Reading the output

```
pid   task   finished(local)          prompt_s    gen_s  total_s   min  ptok  gtok  p_t/s  g_t/s
  1438   2851 2026-11-06T02:51:28+02:00     435.6      61.0    496.7   8.28 40317   905   92.5   14.8
  1438   1292 2026-11-06T02:35:21+02:00      18.1     202.3    220.5   3.67   312  3056   17.2   15.1

calls=28  total=52.51 min  mean=1.88 min  median=1.55 min
min=0.33  p90=3.23  p95=4.23  max=8.28 min
prompt-eval=25.59 min (48%)  gen-eval=26.92 min (51%)
```

| column | meaning |
|---|---|
| `pid` | `avalon-server` process id. Change every restart. |
| `task` | llama.cpp task id. Restart at 0 per launch. Only unique with `pid`. |
| `finished` | Timestamp of `total time` line. When call completed. |
| `prompt_s` / `gen_s` | Seconds on prompt eval and on gen. |
| `total_s` / `min` | Whole call, seconds and minutes. |
| `ptok` / `gtok` | Prompt tokens and gen tokens. |
| `p_t/s` / `g_t/s` | Tokens/s for each phase. |

`total time` count prompt + gen tokens together. Token counts come from prompt-eval and eval lines, not total line.

Times server-side only. Queue, network, client work not included. With `--parallel 1` calls serialize. Sum of `total_s` approx real busy time.

## 4. Measured baseline (RX 7800 XT, `-c 65536`, 2026-11-06)

28 calls, 52.51 min total, mean 1.88 min, median 1.55 min, p90 3.23 min, p95 4.23 min, max 8.28 min. Prompt-eval 48%, gen 51%.

Two calls were third of all time, both prompt-bound: task 2851 (8.28 min, 40317 prompt tokens) and task 0 (4.23 min, 26839 prompt tokens). Gen flat 8–18 t/s. Prompt eval 6–114 t/s, scales with context size. Long context cost more than long answer.

Re-run command in section 2 to refresh numbers. They move as more calls land.

## Troubleshooting

- `No 'total time' lines found` — unit name wrong (`systemctl --user list-units | grep avalon`), journal rotated past calls, or `-o short-iso` omitted so metrics land on one line.
- Nothing from `journalctl --user` — session without user journal (cron, SSH no login). Run from own login, or use `journalctl --user -M "$USER@"` as root.
- Call missing from table — only completed requests log `total time`. Interrupted, cancelled, running calls never appear.
- Duplicate task ids — expected. Task ids restart at 0 each launch. Script keys on `(pid, task)`.
- Prompt eval slow on long prompts — check context size in use. llama.cpp honour only last `-c` when several passed, log `DEPRECATED` for rest.
- Journal huge — narrow with `--since today` or `--since "2026-11-06"`.

## Source

- Parent note: `computer/debian/ai/amd/avalon/README.md`
- [llama.cpp timing output — `slot print_timing`](https://github.com/ggml-org/llama.cpp)
- [systemd — user units and `journalctl --user`](https://wiki.debian.org/Systemd)