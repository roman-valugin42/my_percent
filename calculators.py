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


def calc_payment_distribution(names: list[str], total: float, percent: float) -> dict[str, float]:
    """Распределяет сумму пропорционально количеству вхождений ФИО.

    names  — список ФИО (могут быть дубликаты)
    total  — общая сумма
    percent — процент распределения (0–100)
    """
    counts: dict[str, int] = {}
    for name in names:
        name = name.strip()
        if name:
            counts[name] = counts.get(name, 0) + 1

    total_entries = sum(counts.values())
    if total_entries == 0 or total == 0:
        return {}

    per_entry = (total / total_entries) * (percent / 100)

    return {name: count * per_entry for name, count in counts.items()}
