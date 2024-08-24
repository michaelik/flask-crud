import logging

class LogConfig:
    @staticmethod
    def configure_logging():
        # Create a logger
        logger = logging.getLogger(__name__)

        # Create a console handler for logging
        console_handler = logging.StreamHandler()

        # Define a formatter and attach it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(console_handler)

        # Global log level
        logger.setLevel(logging.DEBUG)

        return logger
