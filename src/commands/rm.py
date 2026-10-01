"""Команда rm — удаление файлов и пустых директорий из VFS."""
from __future__ import annotations

from src.commands.base import Command, CommandContext
from src.vfs import VfsError


class RmCommand(Command):
    name = "rm"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        if ctx.vfs is None:
            return "Ошибка: VFS не загружена"

        if not args:
            return "rm: не указан файл или директория"

        errors: list[str] = []
        for target in args:
            try:
                ctx.vfs.remove(ctx.cwd, target)
            except VfsError as exc:
                errors.append(f"rm: {exc}")

        if errors:
            return "\n".join(errors)
        return ""