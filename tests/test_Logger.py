from python_tracer.Logger import Logger,VerboseLevel

def test_logger():
    try:
        log = Logger("/home/augustin/Documents/Logs/PNG",1,service_name="log", log_extension="log")
        log.info("test info")
        log.debug("test debug")
        log.warning("test warning")
        log.error("test error")
        log.done("test done")
    except Exception as e:
        assert False
        raise
    assert True
test_logger()