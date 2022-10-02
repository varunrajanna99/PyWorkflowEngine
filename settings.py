class EngineConfig:
    """
    Throw all your engine configuration here
    """
    import logging

    bot_location = "./"
    engine_logger = logging.getLogger(__name__)
    engine_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler("WorkflowEngine.log")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    engine_logger.addHandler(file_handler)
    engine_logger.addHandler(stream_handler)