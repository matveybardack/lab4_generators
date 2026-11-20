import os
import random

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

SEED = 12345


@pytest.fixture
def seeded_random():
    random.seed(SEED)
    yield SEED


@pytest.fixture
def valid_lists():
    return [1, 2, 3, 4], [5, 6, 7, 8]
