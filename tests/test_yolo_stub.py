from types import SimpleNamespace

from src.run_yolo_detections import run_yolo_detections


class _FakeModel:
    names = {0: "bottle"}

    def __call__(self, path: str):
        box = SimpleNamespace(cls=[0], conf=[0.9])
        result = SimpleNamespace(boxes=[box])
        return [result]


class _FakeCursor:
    def __init__(self) -> None:
        self.inserts = 0
        self._rows = []

    def execute(self, sql: str, params=None):
        if sql.strip().lower().startswith("insert into raw.image_detections"):
            self.inserts += 1
        elif sql.strip().lower().startswith("select id, file_path from raw.telegram_images"):
            # no-op; fetchall will return preset rows
            pass

    def fetchall(self):
        return list(self._rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConn:
    def __init__(self) -> None:
        self.cursor_obj = _FakeCursor()
        # preset a row with an existing path
        self.cursor_obj._rows = [(1, __file__)]

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass


def test_run_yolo_detections_inserts(monkeypatch):
    # Stub model and filesystem
    monkeypatch.setattr("src.run_yolo_detections.YOLO", lambda _: _FakeModel())
    fake = _FakeConn()

    run_yolo_detections(fake, model_path="ignored.pt")
    assert fake.cursor_obj.inserts >= 1

