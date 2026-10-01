"""Регистр всех команд эмулятора."""
from __future__ import annotations

from src.commands.base import Command, CommandContext
from src.commands.cd import CdCommand
from src.commands.exit import ExitCommand
from src.commands.history import HistoryCommand
from src.commands.ls import LsCommand
from src.commands.uptime import UptimeCommand
from src.commands.vfs_info import VfsInfoCommand
from src.commands.whoami import WhoamiCommand

COMMANDS: dict[str, Command] = {
    "ls": LsCommand(),
    "cd": CdCommand(),
    "exit": ExitCommand(),
    "vfs-info": VfsInfoCommand(),
    "whoami": WhoamiCommand(),
    "history": HistoryCommand(),
    "uptime": UptimeCommand(),
}


def get_command(name: str) -> Command | None:
    """Возвращает команду по имени или None, если команда неизвестна."""
    return COMMANDS.get(name)