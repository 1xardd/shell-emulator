"""Парсер командной строки с раскрытием переменных окружения."""
from __future__ import annotations

import os
import shlex
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """Результат разбора строки ввода."""
    name: str
    args: list[str]


# Соответствие UNIX-подобных переменных и Windows-эквивалентов.
_UNIX_TO_WINDOWS_ENV = {
    "HOME": "USERPROFILE",
    "USER": "USERNAME",
    "SHELL": "COMSPEC",
    "PWD": "CD",
    "PATH": "PATH",
}


def expand_variables(token: str) -> str:
    """Раскрывает переменные окружения в строке.

    Поддерживает:
    - Unix-стиль: $HOME, ${HOME}, $USER
    - Windows-стиль: %USERPROFILE%

    Для Unix-переменных, которых нет в Windows, используется
    таблица соответствий (например, $HOME -> %USERPROFILE%).
    """
    result = token
    # Подставляем Unix-имена на Windows-эквиваленты.
    for unix_name, win_name in _UNIX_TO_WINDOWS_ENV.items():
        # Заменяем $HOME и ${HOME} на %USERPROFILE%
        result = result.replace(f"${{{unix_name}}}", f"%{win_name}%")
        result = result.replace(f"${unix_name}", f"%{win_name}%")
    # Теперь раскрываем Windows-переменные.
    result = os.path.expandvars(result)
    return result


def parse(input_line: str) -> ParsedCommand:
    """Разбирает строку ввода на имя команды и аргументы.

    Поддерживает:
    - одинарные и двойные кавычки;
    - экранирование через \\;
    - раскрытие переменных окружения вида $HOME.
    """
    try:
        tokens = shlex.split(input_line, posix=True)
    except ValueError as exc:
        raise ValueError(f"Ошибка разбора: {exc}") from exc

    if not tokens:
        raise ValueError("Пустая команда")

    name = tokens[0]
    args = [expand_variables(tok) for tok in tokens[1:]]
    return ParsedCommand(name=name, args=args)