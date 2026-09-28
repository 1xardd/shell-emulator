"""Точка входа эмулятора с разбором аргументов командной строки."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_arg_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="shell-emulator",
        description="Эмулятор оболочки ОС (вариант 14).",
    )
    parser.add_argument(
        "--vfs",
        type=Path,
        default=None,
        help="Путь к физическому расположению VFS.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Пользовательское приглашение к вводу (отображается в REPL).",
    )
    parser.add_argument(
        "--script",
        type=Path,
        default=None,
        help="Путь к стартовому скрипту с командами эмулятора.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Выводить отладочную информацию о параметрах запуска.",
    )
    return parser


def print_debug_info(args: argparse.Namespace) -> None:
    """Выводит все параметры запуска в отладочном режиме."""
    print("[DEBUG] Параметры запуска эмулятора:")
    print(f"[DEBUG]   vfs    = {args.vfs}")
    print(f"[DEBUG]   prompt = {args.prompt!r}")
    print(f"[DEBUG]   script = {args.script}")
    print(f"[DEBUG]   debug  = {args.debug}")


def main() -> int:
    """Точка входа."""
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.debug:
        print_debug_info(args)

    # Проверяем существование файлов, если пути заданы
    if args.vfs is not None and not args.vfs.exists():
        print(f"Ошибка: VFS не найдена: {args.vfs}", file=sys.stderr)
        return 1
    if args.script is not None and not args.script.exists():
        print(f"Ошибка: скрипт не найден: {args.script}", file=sys.stderr)
        return 1

    from src.commands.base import CommandContext
    from src.environment import get_hostname, get_username
    from src.script_runner import run_script

    ctx = CommandContext(
        username=get_username(),
        hostname=get_hostname(),
    )

    # Если задан стартовый скрипт — выполняем его.
    if args.script is not None:
        result = run_script(args.script, ctx)

        if result.error is not None:
            print(f"Ошибка скрипта: {result.error}", file=sys.stderr)
            return 1

        # Печатаем диалог: команда и результат.
        for line in result.lines:
            print(f"{ctx.username}@{ctx.hostname}$ {line.source}")
            if line.error is not None:
                print(f"  [пропущено] {line.error}")
            elif line.output:
                print(line.output)

        # Если был exit — завершаем работу.
        if result.exit_requested:
            return 0

    # Запуск GUI
    from src.gui import EmulatorGui

    gui = EmulatorGui(prompt_template=args.prompt)
    gui.run()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())