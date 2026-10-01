"""Команда uptime — сколько времени работает эмулятор."""
from __future__ import annotations

import time

from src.commands.base import Command, CommandContext


class UptimeCommand(Command):
    name = "uptime"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        elapsed = time.time() - ctx.start_time
        return f"Время работы: {self._format_duration(elapsed)}"

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Форматирует длительность в вид 'Xч Yмин Zсек'."""
        total = int(seconds)
        hours, remainder = divmod(total, 3600)
        minutes, secs = divmod(remainder, 60)

        parts: list[str] = []
        if hours:
            parts.append(f"{hours}ч")
        if minutes or hours:
            parts.append(f"{minutes}мин")
        parts.append(f"{secs}сек")
        return " ".join(parts)