"""Информация о реальной ОС (имя пользователя, имя хоста)."""
from __future__ import annotations

import getpass
import socket


def get_username() -> str:
    """Возвращает имя текущего пользователя реальной ОС."""
    try:
        return getpass.getuser()
    except Exception:
        return "unknown"


def get_hostname() -> str:
    """Возвращает имя хоста реальной ОС."""
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def build_title() -> str:
    """Формирует заголовок окна эмулятора.

    Формат: 'Эмулятор - [username@hostname]'
    """
    return f"Эмулятор - [{get_username()}@{get_hostname()}]"