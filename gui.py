"""Модуль с графическим интерфейсом tkinter."""

import tkinter as tk
from tkinter import ttk

from calculators import (
    calc_percent_of,
    calc_percent_ratio,
    calc_increase_decrease,
    calc_payment_distribution,
)


# Mapping названий вкладок → функции и подписи полей
_TABS = {
    "Процент от числа": {
        "func": calc_percent_of,
        "fields": [("X%", None), ("от Y:", None)],
    },
    "Процентное соотношение": {
        "func": calc_percent_ratio,
        "fields": [("X:", None), ("от Y:", None)],
    },
    "Увеличение / уменьшение": {
        "func": lambda val, pct: calc_increase_decrease(val, pct, increase=True),
        "fields": [("Число:", None), ("%:", None)],
    },
    "Уменьшение": {
        "func": lambda val, pct: calc_increase_decrease(val, pct, increase=False),
        "fields": [("Число:", None), ("%:", None)],
    },
}


class PercentCalculator:
    """Главный класс приложения."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Калькулятор процентов")
        self.root.geometry("480x340")
        self.root.resizable(False, False)
        self._apply_styles()
        self._create_widgets()

    def _apply_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#333", font=("Segoe UI", 11))
        style.configure("TEntry", fieldbackground="#fff")
        style.configure("Result.TLabel", font=("Segoe UI", 13, "bold"), foreground="#1a73e8")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#222")
        style.configure("Tab", padding=[12, 6], font=("Segoe UI", 11))

    def _create_widgets(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)

        for title, config in _TABS.items():
            PercentTab(notebook, config["func"], title)

        PaymentTab(notebook, calc_payment_distribution)


class PercentTab:
    """Одна вкладка калькулятора."""

    def __init__(self, parent: ttk.Notebook, calc_func, title: str) -> None:
        self.calc_func = calc_func
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text=title)

        ttk.Label(self.frame, text=title, style="Header.TLabel").pack(pady=(0, 12))

        # Создаём поля ввода динамически
        self.entries: list[ttk.Entry] = []
        fields_config = _TABS[title]["fields"]

        fields_frame = ttk.Frame(self.frame)
        fields_frame.pack(fill=tk.X, pady=4)

        for label_text, _var in fields_config:
            row = ttk.Frame(fields_frame)
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=label_text, width=6, anchor="e").pack(side=tk.LEFT, padx=(0, 8))
            entry = ttk.Entry(row, width=20)
            entry.pack(side=tk.LEFT)
            entry.bind("<Return>", lambda _e: self._calculate())
            self.entries.append(entry)

        # Кнопки
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Вычислить", command=self._calculate).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Очистить", command=self._clear).pack(side=tk.LEFT, padx=4)

        # Результат
        self.result_label = ttk.Label(self.frame, text="—", style="Result.TLabel")
        self.result_label.pack(pady=(8, 0))

    def _calculate(self) -> None:
        values = self._get_values()
        if values is None:
            self.result_label.config(text="Заполните все поля числами.", style="Result.TLabel")
            return

        try:
            result = self.calc_func(*values)
        except ZeroDivisionError:
            self.result_label.config(text="Деление на ноль!", style="Result.TLabel")
            return

        if result is None:
            self.result_label.config(text="Невозможно вычислить.", style="Result.TLabel")
            return

        formatted = str(int(result)) if result == int(result) else f"{result:.4f}".rstrip("0").rstrip(".")
        self.result_label.config(text=f"Результат: {formatted}")

    def _clear(self) -> None:
        for entry in self.entries:
            entry.delete(0, tk.END)
        self.result_label.config(text="—", style="Result.TLabel")

    def _get_values(self) -> list[float] | None:
        values: list[float] = []
        for entry in self.entries:
            text = entry.get().strip()
            if not text:
                return None
            try:
                values.append(float(text))
            except ValueError:
                return None
        return values


class PaymentTab:
    """Вкладка распределения оплаты по ФИО."""

    def __init__(self, parent: ttk.Notebook, calc_func) -> None:
        self.calc_func = calc_func
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Распределение по ФИО")

        ttk.Label(self.frame, text="Распределение оплаты по ФИО",
                  style="Header.TLabel").pack(pady=(0, 12))

        # Поле для списка ФИО
        ttk.Label(self.frame, text="ФИО (каждое с новой строки):").pack(anchor="w", padx=4)
        self.text = tk.Text(self.frame, width=50, height=8, wrap="word")
        self.text.pack(padx=4, pady=(0, 8))

        fields_frame = ttk.Frame(self.frame)
        fields_frame.pack(fill=tk.X, padx=4)

        self.entries: list[ttk.Entry] = []
        fields_config = [("Сумма:", 8), ("%:", 8)]
        for label_text, width in fields_config:
            row = ttk.Frame(fields_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label_text, width=8, anchor="e").pack(side=tk.LEFT, padx=(0, 8))
            entry = ttk.Entry(row, width=width)
            entry.pack(side=tk.LEFT)
            entry.bind("<Return>", lambda _e: self._calculate())
            self.entries.append(entry)

        # Кнопки
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Вычислить", command=self._calculate).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Очистить", command=self._clear).pack(side=tk.LEFT, padx=4)

        self.result_label = ttk.Label(self.frame, text="—", style="Result.TLabel")
        self.result_label.pack(pady=(8, 0))

        # Текст результата
        self.result_text = tk.Text(self.frame, width=50, height=8, wrap="word",
                                   state="disabled", font=("Consolas", 10))
        self.result_text.pack(pady=(0, 8))

    def _calculate(self) -> None:
        names_raw = self.text.get("1.0", tk.END).strip()
        names = [n for n in names_raw.splitlines() if n.strip()]

        values: list[float] = []
        for entry in self.entries:
            text = entry.get().strip()
            if not text:
                return
            try:
                values.append(float(text))
            except ValueError:
                self.result_label.config(text="Некорректные числа.", style="Result.TLabel")
                return

        if not names:
            self.result_label.config(text="Введите хотя бы одно ФИО.", style="Result.TLabel")
            return

        total, percent = values
        result = self.calc_func(names, total, percent)

        if not result:
            self.result_label.config(text="Нет данных для расчёта.", style="Result.TLabel")
            return

        # Формируем текст результата
        lines: list[str] = []
        grand_total = 0.0
        for name, amount in result.items():
            lines.append(f"  {name:<25} {amount:>10.2f}")
            grand_total += amount
        lines.append(f"  {'—' * 34}")
        lines.append(f"  {'Итого:':<25} {grand_total:>10.2f}")

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", "\n".join(lines))
        self.result_text.config(state="disabled")
        self.result_label.config(text=f"Участников: {len(result)}", style="Result.TLabel")

    def _clear(self) -> None:
        self.text.delete("1.0", tk.END)
        for entry in self.entries:
            entry.delete(0, tk.END)
        self.result_label.config(text="—", style="Result.TLabel")
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
