import logging
import csv
from tokenize import Ignore

class CSVReader:
    csvdata = None

    def __init__(self):
        self.csvdata = []
        pass

    def read(self, filepath):
        # opening the CSV file
        with open(filepath, mode='r', encoding='utf-8', errors=Ignore) as file:
            readobj = csv.reader(file)
            if readobj is None:
                logging.warning("File empty")
                return
            try:
                self.csvdata += [lines for lines in readobj]
                logging.debug('Number of elements read: ' + str(len(self.csvdata)))
            except Exception as Argument:
                for lines in readobj:
                    logging.error('Error in: ' + str(lines))
                logging.error('Exception ' + Argument + ' in file: '+ filepath)


    def printData(self):
        for lines in self.csvdata:
            print(lines)

    def getData(self):
        if self.csvdata is []:
            raise Exception('Sorry, data not read yet')
        return self.csvdata
