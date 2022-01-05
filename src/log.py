import logging
# Imports type definition
from logging import Logger

def setup_logger(name: str, log_file: str = None, level: str = 'INFO') -> Logger:
    formatter = "[%(asctime)s] :: [%(levelname)s] :: [%(name)s] :: %(message)s"
    logging.basicConfig(format = formatter,
                        datefmt = "%d-%m-%Y %H:%M:%S",
                        handlers = [
                            logging.StreamHandler()])
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    # If logfile is specified - add file handler and format file log
    if log_file:
        handler = logging.FileHandler(log_file, mode='a')
        handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(handler)

    return logger