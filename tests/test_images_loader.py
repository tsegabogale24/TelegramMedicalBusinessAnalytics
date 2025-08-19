import os
from pathlib import Path
from typing import List, Tuple

from PIL import Image

from src.load_telegram_image import extract_image_metadata, load_image_metadata


def test_extract_image_metadata(tmp_path: Path) -> None:
    img_path = tmp_path / "test.jpg"
    Image.new("RGB", (2, 3), color=(255, 0, 0)).save(img_path)

    meta = extract_image_metadata(str(img_path))
    assert meta is not None
    width, height, size_kb, fmt, mode = meta
    assert (width, height, fmt, mode) == (2, 3, "JPEG", "RGB")
    assert size_kb > 0


class _FakeCursor:
    def __init__(self, rows: List[Tuple] | None = None) -> None:
        self.statements: List[Tuple[str, Tuple]] = []
        self._rows = rows or []

    def execute(self, sql: str, params: Tuple | None = None) -> None:
        self.statements.append((sql.strip(), tuple(params) if params else tuple()))

    def fetchall(self) -> List[Tuple]:
        return list(self._rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConn:
    def __init__(self) -> None:
        self.cursors: List[_FakeCursor] = []
        self.commits = 0

    def cursor(self):
        cur = _FakeCursor()
        self.cursors.append(cur)
        return cur

    def commit(self) -> None:
        self.commits += 1


def test_load_image_metadata_inserts(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "2025-01-01" / "CheMed123"
    base.mkdir(parents=True)
    img_path = base / "x.jpg"
    Image.new("RGB", (4, 5), color=(0, 255, 0)).save(img_path)

    fake = _FakeConn()
    load_image_metadata(fake, base_path=str(tmp_path))

    # One INSERT should have been executed
    executed = [s for cur in fake.cursors for s in cur.statements if s[0].lower().startswith("insert into raw.telegram_images")]
    assert executed, "Expected an INSERT into raw.telegram_images"

