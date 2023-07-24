import sys
import os
import logging

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(logging.LoggerAdapter):
    def __init__(self, logger, error_message, error_detail):
        super().__init__(logger, {})
        self.extra['error_message'] = error_message_detail(error_message, error_detail=error_detail)

    def process(self, msg, kwargs):
        return f"{self.extra['error_message']} - {msg}", kwargs

if __name__ == "__main__":
    # Determine the absolute log file path
    logs_directory = os.path.join(os.getcwd(), "logs")
    log_file_path = os.path.join(logs_directory, "error.log")

    # Create the "logs" directory if it doesn't exist
    os.makedirs(logs_directory, exist_ok=True)

    logging.basicConfig(
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        filename=log_file_path
    )

    try:
        a = 1 / 0
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger = CustomException(logger, e, sys.exc_info())
        logger.error('Divide by Zero')