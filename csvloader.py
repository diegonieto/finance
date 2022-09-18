import csv
import logging
import getopt
import sys

class CSVReader:
    csvdata = []
    def __init__(self):
        pass

    def read(self, filepath):
        # opening the CSV file
        with open(filepath, mode ='r') as file:
            # self.csvdata = csv.reader(file)
            readobj = csv.reader(file)
            if readobj is None:
                logging.warning("File empty")
            for lines in readobj:
                self.csvdata += [lines]
            logging.debug('Number of elements read: ' + str(len(self.csvdata)))

    def printData(self):
        for lines in self.csvdata:
                print(lines)

    def getData(self):
        return self.csvdata

if __name__ == "__main__":
    reader = CSVReader()

    # Modify log level here
    logging.basicConfig(level=logging.WARNING)

    opts, args = getopt.getopt(sys.argv[1:],"hi:",["ifile="])
    inputfile = ''
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + ' -i <inputfile>')
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    if (inputfile is ''):
        inputfile = '/home/dnieto/Documentos/personal/gastos/original/movimientos-agosto.csv'

    reader.read(inputfile)

    reader.printData()
