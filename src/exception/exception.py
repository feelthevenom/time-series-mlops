import sys


class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineo = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame

    def __str__(self):
        return f'{self.error_message} at line {self.lineo} in file {self.file_name}'
        
        
        