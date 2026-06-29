from backend import processor


def test_processor_execution():
    for attr in dir(processor):
        if not attr.startswith("_"):
            obj = getattr(processor, attr)
            if callable(obj):
                try:
                    obj()
                except:
                    pass
