"""Модуль с функциями вычисления процентов."""


def calc_percent_of(a: float, b: float) -> float:
    """X% от Y → результат."""
    return (a / 100) * b


def calc_percent_ratio(a: float, b: float) -> float | None:
    """A — это сколько % от B?"""
    if b == 0:
        return None
    return (a / b) * 100


def calc_increase_decrease(val: float, pct: float, increase: bool = True) -> float:
    """val +/- pct%"""
    if increase:
        return val * (1 + pct / 100)
    return val * (1 - pct / 100)
