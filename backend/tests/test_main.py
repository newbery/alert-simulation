# import pytest

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from backend.main import app
from backend.settings import Settings

client = TestClient(app)
default_settings = jsonable_encoder(Settings())

"""
Some simple tests just confirming that requests to the top level api endpoints
are proxied to the backend implementation as expected.

TODO: The Backend dependency appears resistant to mocking via the typical
dependency injection pattern. No time to investigate this just yet so disabling
most of these tests below for now.
"""


class MockBackend:
    def __init__(self):
        self.calls = []
        self.state = {}

    def __call__(self):
        return self

    def call(self, method, *args, **kwargs):
        print((method, args, kwargs))
        self.calls.append((method, args, kwargs))

    def init(self, *args, **kwargs):
        self.call("init", args, kwargs)

    def ready(self, *args, **kwargs):
        self.call("ready", args, kwargs)
        return {"ready": self.state.get("ready", False)}

    def start(self, *args, **kwargs):
        self.call("start", args, kwargs)

    def status(self, *args, **kwargs):
        self.call("status", args, kwargs)
        return {"status": self.state.get("status", 0)}

    def reset(self, *args, **kwargs):
        self.call("reset", args, kwargs)


def test_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.is_redirect
    assert response.headers.get("Location") == "/app/"


# def test_handle_init(mock_backend):
#     response = client.post("/api/init", json={"settings": default_settings})
#     assert mock_backend.calls == [("init", (), {})]
#     assert response.status_code == 200


# def test_handle_ready(mock_backend):
#     response = client.post("/api/ready", json={"settings": default_settings})
#     assert mock_backend.calls == [("ready", (), {})]
#     assert response.status_code == 200
#     assert response.json() == {"ready": False}

#     mock_backend.state["ready"] = True
#     response = client.post("/api/ready", json={"settings": default_settings})
#     assert mock_backend.calls == [("ready", (), {})]
#     assert response.status_code == 200
#     assert response.json() == {"ready": True}


# def test_handle_start(mock_backend):
#     response = client.post("/api/start", json={"settings": default_settings})
#     assert mock_backend.calls == [("start", (), {})]
#     assert response.status_code == 200


# def test_handle_status(mock_backend):
#     response = client.get("/api/status")
#     assert mock_backend.calls == [("status", (), {})]
#     assert response.status_code == 200
#     assert response.json() == {"status": 0}

#     mock_backend.state["status"] = 10
#     response = client.post("/api/ready", json={"settings": default_settings})
#     assert mock_backend.calls == [("status", (), {})]
#     assert response.status_code == 200
#     assert response.json() == {"status": 10}


# def test_handle_reset(mock_backend):
#     response = client.post("/api/reset")
#     assert mock_backend.calls == [("reset", (), {})]
#     assert response.status_code == 200
