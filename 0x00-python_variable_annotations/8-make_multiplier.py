#!/usr/bin/env python3
"""
Complex types - functions
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    takes a float multiplier as argument and
    returns a function that multiplies a float by multiplier
    """
    def innerfunc(v: float) -> float:
        """
        a function that multiplies
        a float by multiplier
        """
        return float(multiplier * v)
    return innerfunc
