import logging
import csv
import getopt
import sys
import sqlite3
from tokenize import Ignore
from datetime import datetime
import os
import re

# TODO
class DataContainer:
    _isModelSet = False
    _isDataSet = False

    def __init__(self, data) -> None:
        pass

    # Model example
    # { "Date", "Text", "Number" }
    def createModel(self, model = { "Date", "Text", "Number" }):
        self._isModelSet = True

    def plotForecast(self, date):
        if not self._isModelSet:
            logging.error('Model was not set')
        if not self._isDataSet:
            logging.error('Data was not set')

    def setData(self, data):
        self._isDataSet = True


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
        logging.debug('adding ' + values + ' to table ' + table)
        try:
            self._cursor.execute('INSERT INTO ' + table + ' VALUES (' +
                                values + ')')
            self._con.commit()
        except:
            logging.error('Data already exists')

    def createIndex(self, table, index):
        query = 'CREATE INDEX ' + table + '_index' + ' ON ' + table + ' (' + index + ')'
        try:
            self._cursor.execute(query)
        except:
            logging.error('Query error: ' + query)


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

class DatabaseFeeder:
    _reader = None
    _db = None
    _inputDateFormat = '%d/%m/%Y'
    _outputDateFormat = '%Y-%m-%d'
    _costsSchema =  '''
        costs(
            date INT NOT NULL,
            description CHAR (25),
            price REAL,
            PRIMARY KEY(date, price)
            )
        '''
    _accountSchema = '''
        account(
            datetook INT NOT NULL,
            dateasked INT NOT NULL,
            description CHAR (25),
            price REAL,
            balance REAL,
            PRIMARY KEY(price, balance)
            )
    '''

    def __init__(self) -> None:
        self._ddbb = SQLite3Wrapper('finance.db')
        self._ddbb.createTable(self._costsSchema)
        self._ddbb.createTable(self._accountSchema)

    def toJulianday(self, date):
        return 'julianday(\'' + date + '\')'

    def toMoney(self, valueString):
        return valueString.replace(',','.')

    def toPositive(self, valueString):
        return str(float(valueString)*-1.00)

    def parseDate(self, value):
        return self.toJulianday(datetime.strptime(value, self._inputDateFormat).strftime(self._outputDateFormat))

    def _feedAccountWithFileDb(self, inputFile):
        print('Trying to read file: ' + inputFile)
        self._reader = CSVReader()
        self._reader.read(inputFile)
        data = self._reader.getData()

        # model: {date, date, desc, price, balance}
        for line in data:
            dateValue = re.search("\d\d\/\d\d\/.*", line[0])
            if dateValue is not None:
                lineDate1 = self.parseDate(line[0])
                lineDate2 = self.parseDate(line[1])
                lineDesc = line[2].replace('\'',' ')
                values = lineDate1 + ',' + lineDate2 + ',' + '\'' + lineDesc + '\'' + ',' + self.toMoney(line[3]) + ',' + self.toMoney(line[4])
                self._ddbb.insertData('account', values)
                print(values)

    def _feedMovementsWithFileDb(self, inputFile):
        logging.debug('Trying to read file: ' + inputFile)
        self._reader = CSVReader()
        self._reader.read(inputFile)
        data = self._reader.getData()

        # model: {date, desc, price}
        for line in data:
            dateValue = re.search("\d\d\/\d\d\/.*", line[0])
            if dateValue is not None:
                lineDate = self.parseDate(line[0])
                lineDesc = line[1].replace('\'',' ')
                values = lineDate + ',' + '\'' + lineDesc + '\'' + ',' + self.toMoney(line[3])
                self._ddbb.insertData('costs', values)
                print(values)

    def importDataFromDirectory(self, path, type):
        if type is None:
            logging.error('Data type to import not defined')
            raise Exception
        if type == 'costs':
            self._importFilesInPath(path, self._feedMovementsWithFileDb)
        elif type == 'account':
            self._importFilesInPath(path, self._feedAccountWithFileDb)
        else:
            logging.error('Data type not defined')
            raise Exception

    def _importFilesInPath(self, path, feedFunction):
        dataFiles = os.listdir(path)
        for file in dataFiles:
            if file.endswith('.csv'):
                filepath = os.path.join(path, file)
                logging.debug('Trying to import file: ' + filepath)
                feedFunction(filepath)


if __name__ == "__main__":
    dataFeeder = DatabaseFeeder()

    # Force=True because it can be already defined: 
    # https://stackoverflow.com/questions/20240464/python-logging-file-is-not-working-when-using-logging-basicconfig
    logging.basicConfig(filename='csvloader.log', filemode='w',  force=True, level=logging.DEBUG)

    opts, args = getopt.getopt(sys.argv[1:], "hca:", ["accountpath=","costspath="])
    costspath = ''
    accountpath = ''
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + '-c <costs path> -a <account path>')
            exit()
        elif opt in ("-c", "--costsdata"):
            costspath = arg
        elif opt in ("-a", "--accountdata"):
            accountpath = arg

    # TODO remove files with git filterbranch
    if (not ''):
        inputfile = '/tmp/test'

    # dataFeeder.feedMovementsWithFileDb('/tmp/test')

    if accountpath:
        dataFeeder.importDataFromDirectory(accountpath, 'account')
    if costspath:
        dataFeeder.importDataFromDirectory(costspath, 'costs')
