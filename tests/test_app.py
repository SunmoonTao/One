import datetime
import json
import os
import sys
import pytest

# Ensure project root is on sys.path so tests can import app.py
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import get_index_for_date, app, terms


def test_get_index_for_date_consistency():
    # same date should always map to same index
    n = 5
    d = datetime.date(2025, 8, 19)
    i1 = get_index_for_date(n, d)
    i2 = get_index_for_date(n, d)
    assert isinstance(i1, int)
    assert 0 <= i1 < n
    assert i1 == i2


def test_get_index_for_date_wrap():
    n = 3
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 1, 4)  # 3 days later -> index should wrap
    assert get_index_for_date(n, d1) == 0
    assert get_index_for_date(n, d2) == 0


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_api_card_returns_json(client):
    rv = client.get('/api/card')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'index' in data and 'term' in data and 'total' in data
    assert isinstance(data['term'], dict)


def test_api_card_idx_param(client):
    rv = client.get('/api/card?idx=1')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['index'] == 1 % data['total']
