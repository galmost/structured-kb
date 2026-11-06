#!/usr/bin/env python3
"""Per-call cost report for an Avalon / llama.cpp server, read from the journal.

llama-server logs one block per completed request, and each metric sits on its
own journal line:

    slot print_timing: id  0 | task 2851 | prompt eval time = 435601.21 ms / 40317 tokens (   92.51 token per second)
    slot print_timing: id  0 | task 2851 |      eval time = 61000.00 ms / 905 tokens (   14.84 token per second)
    slot print_timing: id  0 | task 2851 |     total time = 496601.21 ms / 41222 tokens

Task ids restart at 0 on every server launch, so calls are keyed on
(pid, task). The `total time` line counts prompt + generated tokens, so token
counts are taken from the prompt-eval and eval lines instead.

Usage:
    journalctl --user -u avalon.service --boot -o short-iso --no-pager | ./avalon_stats.py
    ./avalon_stats.py server.log              # a saved log file instead of stdin
    journalctl --user -u avalon.service ... | ./avalon_stats.py --csv

Stdlib only. Python 3.9+.
"""

import argparse
import re
import statistics
import sys

# Syslog identifier is the binary name: avalon-server[1234] or llama-server[1234].
LINE_RE = re.compile(r"^(\S+).*?(?:avalon|llama)-server\[(\d+)\]:.*task (\d+) \|")
METRIC_RE = re.compile(
    r"\|\s*(prompt eval|(?<!prompt )eval|total) time =\s+([\d.]+) ms /\s+(\d+) tokens"
)


def parse(stream):
    calls = {}
    for line in stream:
        head = LINE_RE.search(line)
        if not head:
            continue
        metric = METRIC_RE.search(line)
        if not metric:
            continue
        key = (head.group(2), int(head.group(3)))
        call = calls.setdefault(key, {"ts": head.group(1)})
        call[metric.group(1)] = (float(metric.group(2)), int(metric.group(3)))
    return sorted(
        ((k, c) for k, c in calls.items() if "total" in c),
        key=lambda item: item[1]["ts"],
    )


def rows(calls):
    for (pid, task), c in calls:
        prompt = c.get("prompt eval", (0.0, 0))
        gen = c.get("eval", (0.0, 0))
        total = c["total"]
        yield {
            "pid": pid,
            "task": task,
            "finished": c["ts"],
            "prompt_s": prompt[0] / 1000,
            "gen_s": gen[0] / 1000,
            "total_s": total[0] / 1000,
            "total_min": total[0] / 60000,
            "prompt_tokens": prompt[1],
            "gen_tokens": gen[1],
            "prompt_tok_s": prompt[1] / (prompt[0] / 1000) if prompt[0] else 0.0,
            "gen_tok_s": gen[1] / (gen[0] / 1000) if gen[0] else 0.0,
        }


def percentile(sorted_values, p):
    idx = min(len(sorted_values) - 1, int(round((p / 100) * (len(sorted_values) - 1))))
    return sorted_values[idx]


HEADER = (
    "pid   task   finished(local)          prompt_s    gen_s  total_s   min"
    "  ptok  gtok  p_t/s  g_t/s"
)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("logfile", nargs="?", help="log file to read instead of stdin")
    ap.add_argument("--csv", action="store_true", help="emit CSV instead of a table")
    args = ap.parse_args()

    src = open(args.logfile) if args.logfile else sys.stdin
    try:
        calls = parse(src)
    finally:
        if args.logfile:
            src.close()

    data = list(rows(calls))
    if not data:
        print(
            "No 'total time' lines found. Feed journalctl output with "
            "-o short-iso, or check the unit name.",
            file=sys.stderr,
        )
        return 1

    if args.csv:
        cols = list(data[0])
        print(",".join(cols))
        for r in data:
            print(",".join(f"{r[c]:.2f}" if isinstance(r[c], float) else str(r[c]) for c in cols))
        return 0

    print(HEADER)
    for r in data:
        print(
            "%6s %6d %-20s %9.1f %9.1f %9.1f  %5.2f %5d %5d  %5.1f  %5.1f"
            % (
                r["pid"], r["task"], r["finished"], r["prompt_s"], r["gen_s"],
                r["total_s"], r["total_min"], r["prompt_tokens"], r["gen_tokens"],
                r["prompt_tok_s"], r["gen_tok_s"],
            )
        )

    totals = sorted(r["total_s"] for r in data)
    prompt_ms = sum(r["prompt_s"] for r in data)
    gen_ms = sum(r["gen_s"] for r in data)
    all_ms = sum(r["total_s"] for r in data)
    print()
    print(
        "calls=%d  total=%.2f min  mean=%.2f min  median=%.2f min"
        % (
            len(totals),
            sum(totals) / 60,
            statistics.mean(totals) / 60,
            statistics.median(totals) / 60,
        )
    )
    print(
        "min=%.2f  p90=%.2f  p95=%.2f  max=%.2f min"
        % (
            totals[0] / 60,
            percentile(totals, 90) / 60,
            percentile(totals, 95) / 60,
            totals[-1] / 60,
        )
    )
    print(
        "prompt-eval=%.2f min (%d%%)  gen-eval=%.2f min (%d%%)"
        % (
            prompt_ms / 60,
            100 * prompt_ms / all_ms,
            gen_ms / 60,
            100 * gen_ms / all_ms,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
