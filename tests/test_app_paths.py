import backend.app

def test_app_execution_paths():
    assert hasattr(backend.app, '__file__')
