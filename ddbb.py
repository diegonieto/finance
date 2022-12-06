from sqlite3wrapper import SQLite3Wrapper
from datetime import datetime

class Database:
    _reader = None
    _ddbb = None
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

    def toEpoch(self, value):
        return datetime.strptime(value, self._outputDateFormat).strftime('%s')

    def toDateformat(self, value):
        return datetime.fromtimestamp(int(value)).strftime(self._outputDateFormat)
