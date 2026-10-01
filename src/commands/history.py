"""Команда history — вывод истории введённых команд."""
from __future__ import annotations

from src.commands.base import Command, CommandContext


class HistoryCommand(Command):
    name = "history"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        if not ctx.history:
            return "(история пуста)"

        lines: list[str] = []
        for index, command in enumerate(ctx.history, start=1):
            lines.append(f"{index:>4}  {command}")
        return "\n".join(lines)