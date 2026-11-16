"""Точка входа — Калькулятор процентов."""

from gui import PercentCalculator


def main() -> None:
    root: object = __import__("tkinter").Tk()
    PercentCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
