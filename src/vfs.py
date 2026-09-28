"""Виртуальная файловая система (VFS) в памяти.

Загружается из XML-файла. Исходный файл НЕ модифицируется —
все данные живут в памяти в виде дерева узлов VfsNode.
"""
from __future__ import annotations

import base64
import hashlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


class VfsError(Exception):
    """Ошибка работы с VFS."""


@dataclass
class VfsNode:
    """Узел VFS — либо файл, либо директория."""
    name: str
    is_dir: bool
    content: bytes = b""
    children: dict[str, "VfsNode"] = field(default_factory=dict)

    def list_names(self) -> list[str]:
        """Возвращает отсортированный список имён дочерних узлов."""
        return sorted(self.children.keys())


class VirtualFileSystem:
    """Виртуальная ФС, загружаемая из XML в память."""

    def __init__(self, name: str, root: VfsNode, raw_bytes: bytes) -> None:
        self.name = name
        self.root = root
        self._hash = hashlib.sha256(raw_bytes).hexdigest()

    # -------------------------------------------------------- свойства

    @property
    def hash_sha256(self) -> str:
        """SHA-256 хеш исходных данных VFS."""
        return self._hash

    # ------------------------------------------------------ загрузка

    @classmethod
    def from_xml(cls, path: Path) -> "VirtualFileSystem":
        """Загружает VFS из XML-файла.

        Args:
            path: путь к XML-файлу.

        Raises:
            VfsError: файл не найден, неверный формат, ошибка парсинга.
        """
        if not path.exists():
            raise VfsError(f"Файл VFS не найден: {path}")

        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise VfsError(f"Не удалось прочитать VFS: {exc}") from exc

        try:
            root_el = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise VfsError(f"Неверный формат XML: {exc}") from exc

        if root_el.tag.lower() != "dir":
            raise VfsError(
                f"Корень VFS должен быть <dir>, а не <{root_el.tag}>"
            )

        root = cls._build_node(root_el)
        return cls(name=path.stem, root=root, raw_bytes=raw)

    @staticmethod
    def _build_node(el: ET.Element) -> VfsNode:
        """Рекурсивно строит узел VFS из XML-элемента."""
        tag = el.tag.lower()
        name = el.get("name")
        if not name:
            raise VfsError(f"У элемента <{tag}> отсутствует атрибут name")

        if tag == "dir":
            node = VfsNode(name=name, is_dir=True)
            for child in el:
                child_node = VirtualFileSystem._build_node(child)
                node.children[child_node.name] = child_node
            return node

        if tag == "file":
            encoded = (el.text or "").strip()
            try:
                data = base64.b64decode(encoded) if encoded else b""
            except Exception as exc:  # noqa: BLE001
                raise VfsError(
                    f"Ошибка декодирования base64 в файле {name}: {exc}"
                ) from exc
            return VfsNode(name=name, is_dir=False, content=data)

        raise VfsError(f"Неизвестный тег: <{tag}>")

    # ---------------------------------------------------- навигация

    def resolve(self, cwd: list[str], target: str = ".") -> VfsNode:
        """Возвращает узел по пути target относительно cwd.

        Поддерживает:
        - "." — текущая директория
        - ".." — родительская
        - "a/b/c" — вложенный путь
        - "/a/b" — абсолютный путь от корня
        """
        if target == "":
            target = "."
        if target == ".":
            return self._resolve_cwd(cwd)
        if target.startswith("/"):
            return self._resolve_absolute(target)

        # Относительный путь от cwd
        node = self._resolve_cwd(cwd)
        for part in target.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                # Родителя в дереве без ссылок не найти — упрощаем:
                # идём от корня заново без последнего элемента cwd.
                # Для простоты ".." обрабатывается на уровне cd.
                continue
            if part not in node.children:
                raise VfsError(f"Нет такого файла или каталога: {target}")
            node = node.children[part]
        return node

    def _resolve_cwd(self, cwd: list[str]) -> VfsNode:
        """Спускается от корня по списку cwd."""
        node = self.root
        for part in cwd:
            if part not in node.children:
                raise VfsError(f"Потеряна часть пути: {part}")
            node = node.children[part]
        return node

    def _resolve_absolute(self, target: str) -> VfsNode:
        """Спускается от корня по абсолютному пути."""
        node = self.root
        for part in target.split("/"):
            if part in ("", "."):
                continue
            if part not in node.children:
                raise VfsError(f"Нет такого файла или каталога: {target}")
            node = node.children[part]
        return node