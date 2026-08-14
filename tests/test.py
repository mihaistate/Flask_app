import pytest
from ..app import index, post, app, get_db_connection
from ..init_db import populate, start, clean


@pytest.fixture()
def db():
    start()
    yield 0
    clean()

def test_index_exists(db):
    app.testing = True
    resp = app.test_client().get("/").data
    assert "marketwatch.com" in str(resp)

def test_newest_exists(db):
    app.testing = True
    resp = app.test_client().get("/newest").data
    assert "ft.com" in str(resp)

def test_get_comment(db):
    app.testing = True
    populate()
    resp = app.test_client().get("/asd").data
    assert "Fritz John" in str(resp)

def test_post_comment(db):
    app.testing = True
    populate()
    resp = app.test_client().post("/asd", data={"user": "Edward King", "body": "Pretty bleak"}, follow_redirects=True).data
    assert "Edward King" in str(resp)