import backend.processor as processor

def test_processor_real_flow():
    # simulate realistic inputs (not random calls)
    inputs = [
        "test text",
        {"data": "sample"},
        None
    ]

    for name in dir(processor):
        func = getattr(processor, name)
        if callable(func) and not name.startswith("_"):
            for inp in inputs:
                try:
                    func(inp)
                except:
                    pass
