# logger.py
import logging

def get_logger(name: str) -> logging.Logger:


    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:

        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setLevel(logging.INFO)


        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)


        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)


        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger