"""GUI-эмулятор оболочки ОС."""
from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext

from src.commands import get_command
from src.commands.base import CommandContext
from src.environment import build_title, get_hostname, get_username
from src.parser import parse

EXIT_MARKER = "__EXIT__"
DEFAULT_PROMPT = "{username}@{hostname}$ "


class EmulatorGui:
    """Графический интерфейс эмулятора."""

    def __init__(
        self,
        prompt_template: str | None = None,
        script_path: str | None = None,
    ) -> None:
        self.ctx = CommandContext(
            username=get_username(),
            hostname=get_hostname(),
        )
        self.prompt_template = prompt_template or DEFAULT_PROMPT
        self.script_path = script_path

        self.root = tk.Tk()
        self.root.title(build_title())
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            self.root,
            state="disabled",
            wrap="word",
            font=("Consolas", 11),
        )
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root, font=("Consolas", 11))
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

        self._print_welcome()
        self._show_prompt()

    # ---------------------------------------------------------------- вывод

    def _print(self, text: str) -> None:
        """Печатает текст в область вывода."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def _print_welcome(self) -> None:
        self._print("Эмулятор оболочки ОС")
        self._print(f"Пользователь: {self.ctx.username}@{self.ctx.hostname}")
        self._print("Введите 'exit' для выхода.")
        self._print("-" * 60)

    def _prompt(self) -> str:
        """Формирует строку приглашения на основе шаблона."""
        try:
            return self.prompt_template.format(
                username=self.ctx.username,
                hostname=self.ctx.hostname,
            )
        except (KeyError, IndexError):
            # Если в шаблоне неизвестный плейсхолдер — возвращаем как есть
            return self.prompt_template

    def _show_prompt(self) -> None:
        self._print(self._prompt())

    # -------------------------------------------------------------- команды

    def _on_enter(self, _event: tk.Event) -> None:
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._print(line)

        if not line.strip():
            self._show_prompt()
            return

        self.ctx.history.append(line)

        try:
            cmd = parse(line)
        except ValueError as exc:
            self._print(f"Ошибка: {exc}")
            self._show_prompt()
            return

        handler = get_command(cmd.name)
        if handler is None:
            self._print(f"Команда не найдена: {cmd.name}")
            self._show_prompt()
            return

        output = handler.execute(self.ctx, cmd.args)

        if output == EXIT_MARKER:
            self.root.destroy()
            return

        if output:
            self._print(output)

        self._show_prompt()

    # ---------------------------------------------------------------- запуск

    def run(self) -> None:
        self.root.mainloop()