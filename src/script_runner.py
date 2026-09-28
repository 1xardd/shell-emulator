"""Выполнение стартовых скриптов эмулятора."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.commands import get_command
from src.commands.base import CommandContext
from src.parser import parse


@dataclass
class ScriptLine:
    """Одна строка скрипта и результат её выполнения."""
    source: str
    output: str = ""
    error: str | None = None


@dataclass
class ScriptResult:
    """Результат выполнения всего скрипта."""
    lines: list[ScriptLine] = field(default_factory=list)
    error: str | None = None
    exit_requested: bool = False


def run_script(
    path: Path,
    ctx: CommandContext,
    exit_marker: str = "__EXIT__",
) -> ScriptResult:
    """Выполняет стартовый скрипт построчно.

    Ошибочные строки пропускаются, но фиксируются в результате.
    """
    result = ScriptResult()

    if not path.exists():
        result.error = f"Скрипт не найден: {path}"
        return result

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.error = f"Не удалось прочитать скрипт: {exc}"
        return result

    for raw_line in text.splitlines():
        source = raw_line.strip()

        if not source or source.startswith("#"):
            continue

        line = ScriptLine(source=source)

        try:
            cmd = parse(source)
        except ValueError as exc:
            line.error = str(exc)
            result.lines.append(line)
            continue

        if cmd.name == "exit":
            line.output = exit_marker
            result.lines.append(line)
            result.exit_requested = True
            return result

        handler = get_command(cmd.name)
        if handler is None:
            line.error = f"Команда не найдена: {cmd.name}"
            result.lines.append(line)
            continue

        try:
            line.output = handler.execute(ctx, cmd.args)
        except Exception as exc:  # noqa: BLE001
            line.error = f"Ошибка выполнения: {exc}"

        result.lines.append(line)

    return result