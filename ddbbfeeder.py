from ddbb import Database
from csvloader import CSVReader
import re
import os
import logging

class DatabaseFeeder(Database):
    _logger = None

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)
        super().__init__()

    def _initFeedTable(self, inputFile):
        self._logger.debug('Trying to read file: ' + inputFile)
        self._reader = CSVReader()
        self._reader.read(inputFile)
        return self._reader.getData()

    def _feedAccountWithFileDb(self, inputFile):
        data = self._initFeedTable(inputFile)

        # model: {date, date, desc, price, balance}
        for line in data:
            dateValue = re.search("\d\d\/\d\d\/.*", line[0])
            if dateValue is not None:
                lineDate1 = self.parseDate(line[0])
                lineDate2 = self.parseDate(line[1])
                lineDesc = line[2].replace('\'',' ')
                values = lineDate1 + ',' + lineDate2 + ',' + '\'' + lineDesc + '\'' + ',' + self.toMoney(line[3]) + ',' + self.toMoney(line[4])
                self._ddbb.insertData('account', values)

    def _feedMovementsWithFileDb(self, inputFile):
        data = self._initFeedTable(inputFile)

        # model: {date, desc, price}
        for line in data:
            dateValue = re.search("\d\d\d\d\-\d\d\-.*", line[0])
            self._logger.error(line[0])
            if dateValue is not None:
                lineDate = self.toJulianday(line[0])
                lineDesc = line[1].replace('\'',' ')
                values = lineDate + ',' + '\'' + lineDesc + '\'' + ',' + self.toMoney(line[3])
                self._ddbb.insertData('costs', values)

    def importDataFromDirectory(self, path, type):
        if type is None:
            self._logger.error('Data type to import not defined')
            raise Exception
        if type == 'costs':
            self._importFilesInPath(path, self._feedMovementsWithFileDb)
        elif type == 'account':
            self._importFilesInPath(path, self._feedAccountWithFileDb)
        else:
            self._logger.error('Data type not defined')
            raise Exception

    def _importFilesInPath(self, path, feedFunction):
        dataFiles = os.listdir(path)
        self._logger.debug('Checking directory ' + path + ' with ' + str(len(dataFiles)) + ' detected')
        
        for file in dataFiles:
            if file.endswith('.csv'):
                filepath = os.path.join(path, file)
                self._logger.debug('Trying to import file: ' + filepath)
                feedFunction(filepath)
