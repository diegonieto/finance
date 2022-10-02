import csv
import logging
import getopt
import sys
import sqlite3
from typing_extensions import Self
from datetime import datetime

class SQLite3Wrapper:
    _con = None
    _cursor = None

    def __init__(self, databasePath) -> None:
        self._con = sqlite3.connect(databasePath)
        self._cursor = self._con.cursor()

    def createTable(self, table):
        try:
            self._cursor.execute('CREATE TABLE ' + table)
        except:
            logging.warning('table already exists')

    def getData(self, table, fields='*', condition=''):
        res = self._cursor.execute('SELECT ' + fields + ' FROM ' + table  + condition)
        return res.fetchall()

    def insertData(self, table, values):
        self._cursor.execute('INSERT INTO ' + table + ' VALUES (' +
                             values + ')')
        self._con.commit()


class CSVReader:
    csvdata = []

    def __init__(self):
        pass

    def read(self, filepath):
        # opening the CSV file
        with open(filepath, mode='r') as file:
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

    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["ifile="])
    inputfile = ''
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + ' -i <inputfile>')
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    if (inputfile == ''):
        inputfile = '/home/dnieto/Documentos/personal/gastos/original/movimientos-agosto.csv'

    reader.read(inputfile)

    data = reader.getData()

    # Database creation
    ddbb = SQLite3Wrapper('finance.db')
    ddbb.createTable('costs(date int not null,description,price)')

    # get date from sql is -> select date(date) from costs

    for line in data:
        if '/' in line[0]:
            lineDate = datetime.strptime(line[0], '%d/%m/%Y').strftime('%Y-%m-%d')
            lineDate = 'julianday(\'' + lineDate + '\')'
            lineDesc = line[1].replace('\'',' ')
            values = lineDate + ',' + '\'' + lineDesc + '\'' + ',' + str(float(line[3].replace(',','.'))*-1.00)
            ddbb.insertData('costs', values)
            print(values)
