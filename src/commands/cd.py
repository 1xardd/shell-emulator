"""Команда cd (заглушка на этапе 1)."""
from __future__ import annotations

from src.commands.base import Command, CommandContext


class CdCommand(Command):
    name = "cd"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        return f"[заглушка] cd вызвана с аргументами: {args}"