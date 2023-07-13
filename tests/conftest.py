from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(__file__).parent / "_fixtures"
