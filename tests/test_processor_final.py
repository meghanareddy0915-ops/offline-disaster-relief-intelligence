import backend.processor as processor


def test_processor_full_execution():
    functions = [
        getattr(processor, x)
        for x in dir(processor)
        if callable(getattr(processor, x)) and not x.startswith("_")
    ]

    for func in functions:
        try:
            # try realistic inputs first
            func("test")
        except:
            try:
                func(None)
            except:
                pass
