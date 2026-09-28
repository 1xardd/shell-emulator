"""Команда exit — завершение работы эмулятора."""
from __future__ import annotations

from src.commands.base import Command, CommandContext

EXIT_MARKER = "__EXIT__"


class ExitCommand(Command):
    name = "exit"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        return EXIT_MARKER