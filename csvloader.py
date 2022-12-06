import logging
import csv
from tokenize import Ignore

class CSVReader:
    _csvdata = None
    _logger = None

    def __init__(self):
        self._csvdata = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)
        super().__init__()

    def read(self, filepath):
        # opening the CSV file
        with open(filepath, mode='r', encoding='utf-8', errors=Ignore) as file:
            readobj = csv.reader(file)
            if readobj is None:
                self._logger.warning("File empty")
                return
            try:
                self._csvdata += [lines for lines in readobj]
                self._logger.debug('Number of elements read: ' + str(len(self._csvdata)))
            except Exception as Argument:
                for lines in readobj:
                    self._logger.error('Error in: ' + str(lines))
                self._logger.error('Exception ' + Argument + ' in file: '+ filepath)


    def printData(self):
        for lines in self._csvdata:
            print(lines)

    def getData(self):
        if self._csvdata is []:
            raise Exception('Sorry, data not read yet')
        return self._csvdata
