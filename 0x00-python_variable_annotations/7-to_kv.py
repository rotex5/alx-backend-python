#!/usr/bin/env python3
"""
Complex types - string andvint/float to tuple
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple:
    """
    takes a string k and an int OR float
    v as arguments returns a tuple
    """
    sq_v: float = v ** 2
    return (k, sq_v)
