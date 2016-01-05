import os
import logging 
from settings import *

class Logger(logging.Logger):

    def __init__(self, name):
        logging.Logger.__init__(self, name)
        self.setLevel(logging.DEBUG)
        
        if not self.handlers:
            file_name = '%s/%s' %(LOG_DIR, name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            self.addHandler(handler)


logging.setLoggerClass(Logger)

