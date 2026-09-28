"""Команда ls — вывод содержимого директории VFS."""
from __future__ import annotations

from src.commands.base import Command, CommandContext
from src.vfs import VfsError


class LsCommand(Command):
    name = "ls"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        if ctx.vfs is None:
            return "Ошибка: VFS не загружена"

        target = args[0] if args else "."

        try:
            node = ctx.vfs.resolve(ctx.cwd, target)
        except VfsError as exc:
            return f"ls: {exc}"

        if not node.is_dir:
            return node.name

        names = node.list_names()
        if not names:
            return ""
        return "\n".join(names)