"""Decorators implemented with functools.wraps."""
from __future__ import annotations
from functools import wraps
from time import perf_counter
from collections.abc import Callable
from typing import Any

def timed(function: Callable[...,Any]) -> Callable[...,Any]:
    @wraps(function)
    def wrapper(*args: Any,**kwargs:Any)->Any:
        start=perf_counter()
        try:return function(*args,**kwargs)
        finally:wrapper.last_elapsed=perf_counter()-start  # type: ignore[attr-defined]
    wrapper.last_elapsed=0.0  # type: ignore[attr-defined]
    return wrapper
