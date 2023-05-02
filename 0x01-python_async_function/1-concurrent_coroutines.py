#!/usr/bin/env python3
"""
Let's execute multiple coroutines
at the same time with async
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    return the list of all the delays
    (float values) arranged in acending order.
    """
    tasks: List = []
    delays: List = []

    for _ in range(n):
        task = asyncio.create_task(wait_random(max_delay))
        tasks.append(task)

    while tasks:
        done, tasks = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            delay = await task
            if not delays or delay >= delays[-1]:
                delays.append(delay)
            else:
                for j, d in enumerate(delays):
                    if delay < d:
                        delays.insert(j, delay)
                        break

    return delays
