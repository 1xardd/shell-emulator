"""Команда ls (заглушка на этапе 1)."""
from __future__ import annotations

from src.commands.base import Command, CommandContext


class LsCommand(Command):
    name = "ls"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        return f"[заглушка] ls вызвана с аргументами: {args}"