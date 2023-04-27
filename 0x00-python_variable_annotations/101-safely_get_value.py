#!/usr/bin/env python3
"""
More involved type annotations
"""
from typing import Any, Mapping, TypeVar, Union


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[TypeVar, None] = None
                     ) -> Union[Any, TypeVar]:
    """
    return duk typed dictioay key or default
    """
    if key in dct:
        return dct[key]
    else:
        return default
