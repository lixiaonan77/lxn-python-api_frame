import pytest
import requests
@pytest.fixture(scope="session")
def token():
    return "test_token_123456"
