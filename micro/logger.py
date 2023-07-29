import logging
import logging.handlers
import os
import pathlib

def logger():
    log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Logs')
    log_location = os.path.join(log_folder,'bot_logs.log')
    if not log_folder:
        os.makedirs(log_folder, exist_ok=True)
    try:
        log_file = open(log_location,'r')
    except:
        log_file = open(log_location,'w')
        log_file.close()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.handlers.RotatingFileHandler(log_location, maxBytes=1048576, backupCount=5)
    logger_handler.setLevel(logging.DEBUG)
    logger_format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    logger_handler.setFormatter(logger_format)
    logger.addHandler(logger_handler)
    logger.info("logger initialised")
    return logger