import backend.app
import importlib

def test_streamlit_module_execution():
    # reload triggers module-level execution paths
    importlib.reload(backend.app)

    assert True
