import pandas as pd
import json
from logg import Logg

class File_Handler:

     def __init__(self):
        self.logger = Logg().get_logger(__name__)
    
     def read_json(self, json_path):
        try:
            with open(json_path) as js:
                json_obj = json.load(js)
            self.logger.info(f'Json file read from {json_path}.')
            return json_obj

        except FileNotFoundError:
            self.logger.exception('File not found.')