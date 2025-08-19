import os
from src.utils.logger import ensure_dir


def test_ensure_dir(tmp_path):
    p = tmp_path / "nested" / "dir"
    ensure_dir(str(p))
    assert os.path.isdir(p)

