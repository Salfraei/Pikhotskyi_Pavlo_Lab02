"""Параметризований декоратор для вимірювання часу виконання."""

from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def measure_time(label: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Вивести тривалість, зберігши сигнатуру оригінальної функції."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = perf_counter()
            result = func(*args, **kwargs)
            elapsed = perf_counter() - start
            print(f"[Таймер] {label}: {elapsed:.8f} с")
            return result

        return wrapper

    return decorator
