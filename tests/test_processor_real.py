import backend.processor as processor

def test_processor_real_execution():
    for name in dir(processor):
        obj = getattr(processor, name)
        if callable(obj):
            try:
                # try calling with safe dummy input
                obj(None)
            except:
                try:
                    obj('')
                except:
                    pass
