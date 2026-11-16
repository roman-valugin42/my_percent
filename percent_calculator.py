"""Десктопное приложение для вычисления процентов."""

import tkinter as tk
from tkinter import ttk


class PercentCalculator:
    """Главный класс приложения — калькулятор процентов."""

    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор процентов")
        self.root.geometry("480x340")
        self.root.resizable(False, False)

        # Стилизация
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TFrame",
            background="#f0f0f0",
        )
        style.configure(
            "TLabel",
            background="#f0f0f0",
            foreground="#333",
            font=("Segoe UI", 11),
        )
        style.configure(
            "TEntry",
            fieldbackground="#fff",
        )
        style.configure(
            "Result.TLabel",
            font=("Segoe UI", 13, "bold"),
            foreground="#1a73e8",
        )
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 14, "bold"),
            foreground="#222",
        )
        style.configure(
            "Tab",
            padding=[12, 6],
            font=("Segoe UI", 11),
        )
        style.configure(
            "Treeview",
            background="#fff",
            fieldbackground="#fff",
            font=("Segoe UI", 10),
        )

        self.create_widgets()

    # ──────────────────────── UI ────────────────────────

    def create_widgets(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        # Вкладки
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Три типа калькуляторов
        PercentTab(self.notebook, self, "Процент от числа", self.calc_percent_of)
        PercentTab(self.notebook, self, "Процентное соотношение", self.calc_percent_ratio)
        PercentTab(self.notebook, self, "Увеличение / уменьшение", self.calc_increase_decrease)

    # ──────────────── общие формулы ─────────────────────

    @staticmethod
    def calc_percent_of(a, b):
        """X% от Y → результат"""
        return (a / 100) * b

    @staticmethod
    def calc_percent_ratio(a, b):
        """A — это сколько % от B?"""
        if b == 0:
            return None
        return (a / b) * 100

    @staticmethod
    def calc_increase_decrease(val, pct, increase=True):
        """val +/- pct%"""
        if increase:
            return val * (1 + pct / 100)
        return val * (1 - pct / 100)


class PercentTab:
    """Одна вкладка калькулятора."""

    def __init__(self, parent, main_app, title, calc_func):
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text=title)

        self.main_app = main_app
        self.calc_func = calc_func

        # Заголовок
        ttk.Label(
            self.frame,
            text=title,
            style="Header.TLabel",
        ).pack(pady=(0, 12))

        # Поля ввода
        self.entries = []
        self.fields_config = self._get_fields_config(title)

        fields_frame = ttk.Frame(self.frame)
        fields_frame.pack(fill=tk.X, pady=4)

        for label_text, var in self.fields_config:
            row = ttk.Frame(fields_frame)
            row.pack(fill=tk.X, pady=3)

            ttk.Label(row, text=label_text, width=6, anchor="e").pack(side=tk.LEFT, padx=(0, 8))
            entry = ttk.Entry(row, width=20)
            entry.pack(side=tk.LEFT)
            entry.bind("<Return>", lambda _e: self._calculate())
            self.entries.append(entry)

        # Кнопка
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Вычислить",
            command=self._calculate,
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=4)

        ttk.Button(
            btn_frame,
            text="Очистить",
            command=self._clear,
        ).pack(side=tk.LEFT, padx=4)

        # Результат
        self.result_label = ttk.Label(
            self.frame,
            text="—",
            style="Result.TLabel",
        )
        self.result_label.pack(pady=(8, 0))

    def _get_fields_config(self, title):
        """Возвращает список (подпись, tk.StringVar) для полей ввода."""
        if title == "Процент от числа":
            return [
                ("X%", tk.StringVar()),
                ("от Y:", tk.StringVar()),
            ]
        elif title == "Процентное соотношение":
            return [
                ("X:", tk.StringVar()),
                ("от Y:", tk.StringVar()),
            ]
        else:
            return [
                ("Число:", tk.StringVar()),
                ("%:", tk.StringVar()),
            ]

    def _calculate(self):
        values = self._get_values()
        if values is None:
            self.result_label.config(text="Пожалуйста, заполните все поля числами.", style="Result.TLabel")
            return

        try:
            result = self.calc_func(*values)
        except ZeroDivisionError:
            self.result_label.config(text="Деление на ноль!", style="Result.TLabel")
            return

        if result is None:
            self.result_label.config(text="Невозможно вычислить.", style="Result.TLabel")
            return

        # Форматирование результата
        if result == int(result):
            formatted = str(int(result))
        else:
            formatted = f"{result:.4f}".rstrip("0").rstrip(".")

        self.result_label.config(text=f"Результат: {formatted}")

    def _clear(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
        self.result_label.config(text="—", style="Result.TLabel")

    def _get_values(self):
        """Парсит все поля ввода в list[float]. Возвращает None при ошибке."""
        values = []
        for entry in self.entries:
            text = entry.get().strip()
            if not text:
                return None
            try:
                values.append(float(text))
            except ValueError:
                return None
        return values


# ──────────────── запуск ────────────────────────

def main():
    root = tk.Tk()
    app = PercentCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
