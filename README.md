# Эмулятор оболочки ОС

Учебный проект по дисциплине **«Конфигурационное управление»**.
**Вариант №14** — эмулятор командной оболочки UNIX-подобной ОС.

**Автор:** Kryuk (GitHub: [@1xardd](https://github.com/1xardd))
**Репозиторий:** https://github.com/1xardd/shell-emulator
**Учебное заведение:** РТУ МИРЭА
**Группа:** ИКБО-65-25
**Семестр:** 3 семестр (осенний) 2026/2027 учебного года
**Преподаватель:** Горчаков А.В.

---

## Требования

- Python 3.10+
- tkinter (входит в стандартную поставку Python)

## Запуск

### Запуск GUI

```bash
python -m src.main
```

Откроется окно `Эмулятор - [kryuk@Maria]` с приглашением `kryuk@Maria$ `.

### С VFS

```bash
python -m src.main --vfs vfs/deep_tree.xml
```

### С пользовательским приглашением

```bash
python -m src.main --prompt "[{username}@{hostname}] $ "
```

### Со стартовым скриптом

```bash
python -m src.main --script scripts/demo_commands.txt
```

### Отладочный режим

```bash
python -m src.main --debug
```

### Примеры .ps1-обёрток

```powershell
.\scripts\run_minimal.ps1           # запуск по умолчанию
.\scripts\run_with_prompt.ps1       # с приглашением
.\scripts\run_with_script.ps1       # со скриптом команд
.\scripts\run_vfs_minimal.ps1       # с минимальной VFS
.\scripts\run_vfs_few_files.ps1     # с VFS из нескольких файлов
.\scripts\run_vfs_deep.ps1          # с глубокой VFS и скриптом
.\scripts\run_stage4.ps1            # тест whoami/history/uptime
.\scripts\run_stage5.ps1            # тест rm
```

## Параметры командной строки

| Параметр    | Описание                                              |
|-------------|-------------------------------------------------------|
| `--vfs`     | Путь к физическому расположению VFS (XML)             |
| `--prompt`  | Пользовательское приглашение к вводу (для REPL)       |
| `--script`  | Путь к стартовому скрипту с командами эмулятора       |
| `--debug`   | Выводить отладочную информацию о параметрах запуска   |

## Плейсхолдеры в `--prompt`

- `{username}` — имя пользователя реальной ОС (у меня `kryuk`)
- `{hostname}` — имя хоста реальной ОС (у меня `Maria`)

## Команды

- `ls [path]` — список содержимого директории VFS
- `cd [path]` — переход в директорию VFS
- `rm [path...]` — удаление файлов и пустых директорий
- `whoami` — имя текущего пользователя (`kryuk`)
- `history` — история введённых команд
- `uptime` — время работы эмулятора
- `vfs-info` — информация о загруженной VFS (имя + SHA-256)
- `exit` — выход из эмулятора

## Возможности

- GUI-интерфейс (tkinter)
- Парсер с поддержкой кавычек и экранирования
- Раскрытие переменных окружения: `$HOME`, `$USER`, `${HOME}`, `%USERPROFILE%`
- Виртуальная файловая система (VFS) из XML, работающая в памяти
- Вычисление SHA-256 от исходных данных VFS
- Навигация и модификация VFS (ls, cd, rm) без изменения источника
- Выполнение стартовых скриптов с пропуском ошибочных строк
- Настраиваемое приглашение к вводу
- Отладочный вывод параметров запуска

## Пример работы

```
kryuk@Maria$ whoami
kryuk
kryuk@Maria$ vfs-info
Имя VFS: deep_tree
SHA-256: 07353713ffdf45a89badd1529d14205aa243e0c67a29ea55762cf883fbc414ae
kryuk@Maria$ ls
etc
home
motd.txt
kryuk@Maria$ rm motd.txt
kryuk@Maria$ ls
etc
home
kryuk@Maria$ rm motd.txt
rm: Нет такого файла или каталога: motd.txt
kryuk@Maria$ rm home
rm: Директория не пуста: home
kryuk@Maria$ uptime
Время работы: 18сек
kryuk@Maria$ history
   1  whoami
   2  vfs-info
   3  ls
   4  rm motd.txt
   5  ls
   6  rm motd.txt
   7  rm home
   8  uptime
   9  history
kryuk@Maria$ exit
```

## Тестовые VFS

В папке `vfs/` лежат три тестовые файловые системы:

| Файл             | Содержимое                                    | SHA-256 (для проверки) |
|------------------|-----------------------------------------------|------------------------|
| `minimal.xml`    | 1 файл в корне                                | `8c13ff1ade9f28b1cbc4f37caae6c2dbd0d29d5144997e35528a278da399e5cc` |
| `few_files.xml`  | 3 файла + папка `docs`                        | — |
| `deep_tree.xml`  | 4 уровня вложенности, файлы и папки           | `07353713ffdf45a89badd1529d14205aa243e0c67a29ea55762cf883fbc414ae` |

## Этапы разработки

| Этап | Что реализовано | Коммит |
|------|-----------------|--------|
| 1 | REPL + GUI + парсер + заглушки `ls`/`cd` + `exit` | `d9783f1` |
| 2 | CLI-параметры + стартовые скрипты + `.ps1`-обёртки | `15b4144d` |
| — | Обновление README для этапа 2 | `354c19f` |
| 3 | VFS из XML + `vfs-info` + реальные `ls`/`cd` | `99d9a1e` |
| 4 | `whoami`, `history`, `uptime` | `1eeb9f0` |
| 5 | `rm` с модификацией VFS только в памяти | `b17a64f` |

## Структура проекта

```
.
├── src/
│   ├── commands/          # команды эмулятора
│   │   ├── __init__.py    # регистр команд
│   │   ├── base.py        # базовый класс команды и контекст
│   │   ├── cd.py          # команда cd
│   │   ├── exit.py        # команда exit
│   │   ├── history.py     # команда history
│   │   ├── ls.py          # команда ls
│   │   ├── rm.py          # команда rm
│   │   ├── uptime.py      # команда uptime
│   │   ├── vfs_info.py    # команда vfs-info
│   │   └── whoami.py      # команда whoami
│   ├── __init__.py
│   ├── environment.py     # данные реальной ОС
│   ├── gui.py             # графический интерфейс
│   ├── main.py            # точка входа, разбор CLI
│   ├── parser.py          # парсер команд
│   ├── script_runner.py   # выполнение стартовых скриптов
│   └── vfs.py             # виртуальная файловая система
├── vfs/                   # тестовые VFS (XML)
│   ├── minimal.xml
│   ├── few_files.xml
│   └── deep_tree.xml
├── scripts/               # примеры скриптов запуска и команд
│   ├── demo_commands.txt
│   ├── demo_commands4.txt
│   ├── demo_commands5.txt
│   ├── demo_vfs.txt
│   ├── run_minimal.ps1
│   ├── run_with_prompt.ps1
│   ├── run_with_script.ps1
│   ├── run_vfs_minimal.ps1
│   ├── run_vfs_few_files.ps1
│   ├── run_vfs_deep.ps1
│   ├── run_stage4.ps1
│   └── run_stage5.ps1
├── .gitignore
└── README.md
```

## Лицензия

Учебный проект. Свободное использование в образовательных целях.