"""Команда cd — смена текущей директории в VFS."""
from __future__ import annotations

from src.commands.base import Command, CommandContext
from src.vfs import VfsError


class CdCommand(Command):
    name = "cd"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        if ctx.vfs is None:
            return "Ошибка: VFS не загружена"

        # cd без аргументов — переход в корень
        target = args[0] if args else "/"

        if target == "..":
            if ctx.cwd:
                ctx.cwd.pop()
            return ""

        if target == "/" or target == ".":
            if target == "/":
                ctx.cwd.clear()
            return ""

        # Абсолютный путь — начинаем от корня
        if target.startswith("/"):
            new_cwd: list[str] = []
            parts = [p for p in target.split("/") if p]
        else:
            new_cwd = list(ctx.cwd)
            parts = [p for p in target.split("/") if p]

        for part in parts:
            if part == "..":
                if new_cwd:
                    new_cwd.pop()
                continue
            if part == ".":
                continue

            try:
                node = ctx.vfs.resolve(new_cwd, part)
            except VfsError as exc:
                return f"cd: {exc}"

            if not node.is_dir:
                return f"cd: не директория: {part}"

            new_cwd.append(part)

        ctx.cwd = new_cwd
        return ""