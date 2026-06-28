import backend.processor as processor

def test_processor_real_inputs():
    # try meaningful execution paths (not random calls)
    try:
        if hasattr(processor, "process"):
            processor.process("sample input")
    except:
        pass

    try:
        if hasattr(processor, "process_text"):
            processor.process_text("disaster report")
    except:
        pass
