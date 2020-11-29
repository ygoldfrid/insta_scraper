import logging

logger = logging.getLogger('insta_logger')
logger_file = logging.getLogger('insta_logger.file')
logger_console = logging.getLogger('insta_logger.console')
logger_fc = logging.getLogger('insta_logger.fc')


def configure():
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('insta_scraper.log', encoding="UTF-8")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger_file.addHandler(file_handler)
    logger_console.addHandler(console_handler)

    logger_fc.addHandler(file_handler)
    logger_fc.addHandler(console_handler)


CONSOLE = 1
FILE = 2


def log(level, msg, destination=(CONSOLE | FILE)):
    current_logger = logger_fc

    if destination == CONSOLE:
        current_logger = logger_console
    elif destination == FILE:
        current_logger = logger_file
    elif destination != (FILE | CONSOLE):
        raise ValueError('Invalid destination level: %s' % destination)

    # output log message
    if level == logging.DEBUG:
        current_logger.debug(msg)
    elif level == logging.INFO:
        current_logger.info(msg)
    elif level == logging.WARNING:
        current_logger.warning(msg)
    elif level == logging.ERROR:
        current_logger.error(msg)
    elif level == logging.CRITICAL:
        current_logger.critical(msg)
    else:
        raise ValueError('Invalid log level: %s' % level)
