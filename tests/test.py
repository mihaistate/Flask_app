from urllib import response
import pytest
import sys
from ..app import index, post, app
from ..init_db import start
import sqlite3

def test_index_exists():
    start()
    app.testing = True
    resp = app.test_client().get("/").data
    assert "marketwatch.com" in str(resp)

def test_newest_exists():
    start()
    app.testing = True
    resp = app.test_client().get("/newest").data
    assert "ft.com" in str(resp)


def test_newest_exists():
    start()
    app.testing = True
    resp = app.test_client().get("/newest").data
    assert "ft.com" in str(resp)