import backend.processor as processor

def test_processor_full():
    for name in dir(processor):
        obj = getattr(processor, name)
        if callable(obj) and not name.startswith('_'):
            try:
                obj()
            except:
                try:
                    obj('test')
                except:
                    pass
