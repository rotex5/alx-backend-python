#!/usr/bin/env python3
"""
Measure the runtime
"""
import asyncio
from time import perf_counter

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    measures the total execution time for
    wait_n(n, max_delay), and returns total_time / n.
    """
    s: float = perf_counter()

    asyncio.run(wait_n(n, max_delay))

    elapsed: float = perf_counter() - s
    _time: float = elapsed / n

    return _time
