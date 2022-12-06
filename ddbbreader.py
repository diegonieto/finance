from ddbb import Database
import logging


class DatabaseReader(Database):
    _accountData = '''
        date(datetook),
        description,
        price,
        balance
    '''
    def getAllAccountData(self):
        return self._ddbb.getData(
            'account', 
            self._accountData, 
            'order by datetook'
            )
