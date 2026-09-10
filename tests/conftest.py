import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Snapshot of the original in-memory activities so each test starts fresh
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    yield TestClient(app)
    # Restore state so mutations from one test don't leak into the next
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
