"""Базовый класс команды и контекст выполнения."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class CommandContext:
    """Общий контекст выполнения команд.

    Здесь хранится всё, что нужно командам: имя пользователя,
    имя хоста, история команд. На следующих этапах сюда
    добавится виртуальная файловая система и текущая директория.
    """
    username: str
    hostname: str
    history: list[str] = field(default_factory=list)


class Command(ABC):
    """Абстрактная команда эмулятора."""
    name: str = ""

    @abstractmethod
    def execute(self, ctx: CommandContext, args: list[str]) -> str:
        """Выполняет команду.

        Возвращает текст, который надо вывести пользователю.
        Специальное значение '__EXIT__' означает завершение работы.
        """
        ...