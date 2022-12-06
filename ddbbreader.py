from ddbb import Database


class DatabaseReader(Database):
    _accountData = '''
        CAST(strftime('%s', datetook) AS INT),
        description,
        price,
        balance
    '''
    def getAllAccountData(self, fromDate=''):
        return self._ddbb.getData(
            'account', 
            self._accountData, 
            'where datetook > ' + self.toJulianday(fromDate),
            'order by datetook',
            )
