"""Команда whoami — вывод имени текущего пользователя."""
from __future__ import annotations

from src.commands.base import Command, CommandContext


class WhoamiCommand(Command):
    name = "whoami"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        return ctx.username