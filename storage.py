import json
import pickle
from library import Library

from vars import DATA_PATH


class StorageUtil:
    
    library = None
    
    def __init__(self):
        try:
            with open(DATA_PATH, 'rb') as f:
                self.library = pickle.load(f)
        except IOError:
            pass
        except pickle.UnpicklingError:
            pass
        
    def get_library(self):
        return self.library
    
    def save_library(self, library):
        with open(DATA_PATH, 'wb') as f:
            pickle.dump(library, f)
