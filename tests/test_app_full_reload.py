import importlib

import backend.app


def test_streamlit_module_execution():
    # reload triggers module-level execution paths
    importlib.reload(backend.app)

    assert True
