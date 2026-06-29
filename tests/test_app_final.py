import backend.app


def test_app_force_paths():
    # simulate streamlit import execution paths
    assert hasattr(backend.app, "__file__")

    # force module-level execution
    import importlib

    importlib.reload(backend.app)
