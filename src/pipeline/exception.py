import sys
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