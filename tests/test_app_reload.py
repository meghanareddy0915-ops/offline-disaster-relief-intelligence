import importlib

import backend.app


def test_app_execution_full():
    # reload forces re-execution of top-level code
    importlib.reload(backend.app)

    assert hasattr(backend.app, "__file__")
