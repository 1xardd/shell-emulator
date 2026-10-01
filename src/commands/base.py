"""Базовый класс команды и контекст выполнения."""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.vfs import VirtualFileSystem


@dataclass
class CommandContext:
    """Общий контекст выполнения команд.

    Здесь хранится всё, что нужно командам: имя пользователя,
    имя хоста, история команд, VFS, текущая директория,
    время запуска эмулятора.
    """
    username: str
    hostname: str
    vfs: "VirtualFileSystem | None" = None
    cwd: list[str] = field(default_factory=list)
    history: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)


class Command(ABC):
    """Абстрактная команда эмулятора."""
    name: str = ""

    @abstractmethod
    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        """Выполняет команду. Возвращает текст для вывода."""
        ...