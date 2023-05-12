import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)03d [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler('app/logs/debug.log'),
        logging.StreamHandler()
    ])


def get_logger(class_name):
    return logging.getLogger(class_name)