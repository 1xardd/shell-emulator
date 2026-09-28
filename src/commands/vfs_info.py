"""Служебная команда vfs-info — информация о загруженной VFS."""
from __future__ import annotations

from src.commands.base import Command, CommandContext


class VfsInfoCommand(Command):
    name = "vfs-info"

    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        vfs = getattr(ctx, "vfs", None)
        if vfs is None:
            return "Ошибка: VFS не загружена"
        return f"Имя VFS: {vfs.name}\nSHA-256: {vfs.hash_sha256}"