#!/usr/bin/env python3
"""Simple benchmark runner for MCPturbo.

The script executes a dummy asynchronous task multiple times to estimate
latency percentiles (p50/p95), throughput, memory usage and approximate
cost per task. Replace ``sample_task`` with real MCPturbo operations to
benchmark your own workload.

Example:
    python bench.py --tasks 100 --concurrency 10 --usd-per-second 0.02
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from typing import List

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - psutil is optional
    psutil = None


async def sample_task() -> None:
    """Simulate work. Replace with a real MCPturbo request."""
    await asyncio.sleep(0.01)


def memory_usage_mb() -> float:
    """Return current process memory in megabytes."""
    if psutil is not None:
        return psutil.Process().memory_info().rss / (1024**2)
    import resource

    # ru_maxrss is in kilobytes on Linux
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


async def run_benchmark(tasks: int, concurrency: int) -> dict:
    latencies: List[float] = []
    sem = asyncio.Semaphore(concurrency)

    async def run_one(_: int) -> None:
        async with sem:
            start = time.perf_counter()
            await sample_task()
            end = time.perf_counter()
            latencies.append(end - start)

    start_time = time.perf_counter()
    await asyncio.gather(*(run_one(i) for i in range(tasks)))
    total_time = time.perf_counter() - start_time

    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[int(0.95 * len(latencies)) - 1]
    throughput = tasks / total_time if total_time > 0 else float("inf")

    return {
        "tasks": tasks,
        "duration_s": total_time,
        "latency_ms_p50": p50 * 1000,
        "latency_ms_p95": p95 * 1000,
        "throughput_tps": throughput,
        "memory_mb": memory_usage_mb(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MCPturbo benchmarks")
    parser.add_argument("--tasks", type=int, default=100, help="Number of tasks to execute")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent tasks to run")
    parser.add_argument(
        "--usd-per-second",
        type=float,
        default=0.0,
        help="Cost rate in USD per second of runtime",
    )
    args = parser.parse_args()

    report = asyncio.run(run_benchmark(args.tasks, args.concurrency))
    total_cost = report["duration_s"] * args.usd_per_second
    report["cost_per_task_usd"] = total_cost / args.tasks if args.tasks else 0.0

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
