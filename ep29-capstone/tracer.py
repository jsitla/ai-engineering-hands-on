"""A tiny tracer: time each step, remember extra facts, and save everything to traces.jsonl."""
import json
import time
from contextlib import contextmanager
from pathlib import Path

LOG = Path(__file__).with_name("traces.jsonl")
_spans = []


@contextmanager
def span(name, **info):
    start = time.perf_counter()
    record = {"name": name, **info}
    try:
        yield record          # the step can add facts, like token counts
    finally:
        record["ms"] = round((time.perf_counter() - start) * 1000, 1)
        _spans.append(record)


def save_and_show(trace_name):
    total = sum(s["ms"] for s in _spans)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"trace": trace_name, "spans": _spans}) + "\n")
    print(f"trace: {trace_name}  ({total / 1000:.2f} s)")
    for s in _spans:
        bar = "#" * max(1, round(40 * s["ms"] / total))
        extra = {k: v for k, v in s.items() if k not in ("name", "ms")}
        print(f"  {s['name']:<18} {s['ms']:>8.1f} ms  {bar:<40} {extra if extra else ''}")
    _spans.clear()
