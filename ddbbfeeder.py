from ddbb import Database
from csvloader import CSVReader
import re
import os
import logging

class DatabaseFeeder(Database):
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
