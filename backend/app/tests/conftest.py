import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["HERMES_DB_PATH"] = str(Path(__file__).resolve().parent / "test_hermesforge.db")

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
