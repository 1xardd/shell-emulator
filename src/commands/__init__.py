"""Регистр всех команд эмулятора."""
from __future__ import annotations

from src.commands.base import Command, CommandContext
from src.commands.cd import CdCommand
from src.commands.exit import ExitCommand
from src.commands.ls import LsCommand
from src.commands.vfs_info import VfsInfoCommand

COMMANDS: dict[str, Command] = {
    "ls": LsCommand(),
    "cd": CdCommand(),
    "exit": ExitCommand(),
    "vfs-info": VfsInfoCommand(),
}


def get_command(name: str) -> Command | None:
    """Возвращает команду по имени или None, если команда неизвестна."""
    return COMMANDS.get(name)