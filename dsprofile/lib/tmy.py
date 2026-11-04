#imports
import sys
from dsprofile.lib.reader import Reader
from pvlib.iotools import read_tmy3

#subclass
class TMYReader(Reader):
    format = "tmy"

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.dataset = self.read_dataset(filename)

    @staticmethod
    def read_dataset(filename):
        try:
            data, meta = read_epw(filename)
        except (OSError, PermissionError, FileNotFoundError) as e:
            print(f"Unable to read dataset '{filename}': {e}", file=sys.stderr)
            sys.exit(1)
        
        return dataset

