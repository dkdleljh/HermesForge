import os
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient

_test_directory = TemporaryDirectory(prefix="hermesforge-tests-")
os.environ["HERMES_DB_PATH"] = _test_directory.name + "/test.sqlite"

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
