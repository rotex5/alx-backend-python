#!/usr/bin/env python3
"""
The Basics of async
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
     waits for a random delay between 0 and max_delay
     (included and float value) seconds and eventually
     returns it.
    """
    i = random.uniform(0, max_delay)
    await asyncio.sleep(i)
    return i
