import logging


class MyLogger:
    def __init__(
        self,
        log_file: str,
        log_level: int = logging.INFO,
        log_name: str = __name__
    ):

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(message)s')
        self.file_handler = logging.FileHandler(log_file)
        self.stream_handler = logging.StreamHandler()

        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def critical(self, message: str):
        self.logger.critical(message)
