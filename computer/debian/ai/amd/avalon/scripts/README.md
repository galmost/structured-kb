# Avalon Call Stats Scripts (Debian 13 "trixie")

`avalon_stats.py` turns the `avalon.service` journal into a per-call cost
report: how many minutes each completed request took, split into prompt-eval
and generation time, plus mean/median/percentiles and the prompt-vs-generation
split. Use it to find which calls dominate wall time and whether a call is
prompt-bound or generation-bound.

Stdlib only, Python 3.9+. No root needed: `avalon.service` is a systemd
*user* unit, so `journalctl --user` reads it.

## 1. Prerequisites

- `avalon.service` running as a user unit
  (`~/.config/systemd/user/avalon.service`, see the parent note
  `computer/debian/ai/amd/avalon`).
- `python3` (3.9+).
- Journal entries emitted by `llama-server` at its default log level. The
  lines the script needs look like this:

```
slot print_timing: id  0 | task 2851 | prompt eval time = 435601.21 ms / 40317 tokens (   92.51 token per second)
slot print_timing: id  0 | task 2851 |      eval time = 61000.00 ms / 905 tokens (   14.84 token per second)
slot print_timing: id  0 | task 2851 |     total time = 496601.21 ms / 41222 tokens
```

Each metric is on its own journal line, so pass `-o short-iso` to get one
timestamp per line.

## 2. Run it

Current boot:

```bash
journalctl --user -u avalon.service --boot -o short-iso --no-pager | ./avalon_stats.py
```

Every boot in the journal (more calls, but task ids repeat across launches —
the script keys on PID + task, so they stay separate):

```bash
journalctl --user -u avalon.service -o short-iso --no-pager | ./avalon_stats.py
```

Machine-readable output, for plotting or feeding into another tool:

```bash
journalctl --user -u avalon.service --boot -o short-iso --no-pager | ./avalon_stats.py --csv
```

A saved log file instead of the live journal:

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
| `pid` | `avalon-server` process id. Changes on every restart. |
| `task` | llama.cpp task id. Restarts at 0 per launch, so only unique with `pid`. |
| `finished` | Timestamp of the `total time` line, i.e. when the call completed. |
| `prompt_s` / `gen_s` | Seconds spent on prompt eval and on generation. |
| `total_s` / `min` | Whole call, seconds and minutes. |
| `ptok` / `gtok` | Prompt tokens and generated tokens. |
| `p_t/s` / `g_t/s` | Tokens/s for each phase. |

`total time` counts prompt + generated tokens together, so token counts come
from the prompt-eval and eval lines, not the total line.

Times are server-side processing only. Queueing, network, and client-side
work are not included. With `--parallel 1` calls serialize, so the sum of
`total_s` approximates real busy time.

## 4. Measured baseline (RX 7800 XT, `-c 65536`, 2026-11-06)

28 calls, 52.51 min total, mean 1.88 min, median 1.55 min, p90 3.23 min,
p95 4.23 min, max 8.28 min. Prompt-eval 48%, generation 51%.

Two calls were a third of all time, both prompt-bound: task 2851 (8.28 min,
40317 prompt tokens) and task 0 (4.23 min, 26839 prompt tokens). Generation
runs a fairly flat 8–18 t/s; prompt eval ranges 6–114 t/s and scales with
context size. Long context costs more than long answers.

Re-run the command in section 2 to refresh these numbers; they move as more
calls land.

## Troubleshooting

- `No 'total time' lines found` — either the unit name is wrong
  (`systemctl --user list-units | grep avalon`), the journal was rotated past
  the calls, or `-o short-iso` was omitted so metrics land on one line.
- Nothing from `journalctl --user` — you are in a session without a user
  journal (cron, SSH without a login session). Run it from your own login, or
  use `journalctl --user -M "$USER@"` as root.
- A call is missing from the table — only completed requests log `total time`.
  Interrupted, cancelled, or still-running calls never appear.
- Duplicate task ids — expected. Task ids restart at 0 on each server launch;
  the script keys on `(pid, task)`.
- Prompt eval much slower than expected on long prompts — check the context
  size actually in use. llama.cpp honours only the last `-c` when several are
  passed and logs `DEPRECATED` for the rest.
- Journal is huge — narrow with `--since today` or `--since "2026-11-06"`.

## Source

- Parent note: `computer/debian/ai/amd/avalon/README.md`
- [llama.cpp timing output — `slot print_timing`](https://github.com/ggml-org/llama.cpp)
- [systemd — user units and `journalctl --user`](https://wiki.debian.org/Systemd)
