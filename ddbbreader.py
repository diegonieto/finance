from ddbb import Database


class DatabaseReader(Database):
    _accountData = '''
        CAST(strftime('%s', datetook) AS INT),
        description,
        price,
        balance
    '''

    _costsData = '''
        CAST(strftime('%s', date) AS INT),
        description,
        price
    '''

    def _getDateRange(self, field, fromDate, toDate):
        fromDateClause = ''
        toDateClause = ''
        dateRange = ''
        if fromDate:
            fromDateClause = ' ' + field + ' > ' + self.toJulianday(fromDate)
        if toDate:
            toDateClause = ' ' + field + ' < ' + self.toJulianday(toDate)

        if fromDateClause and toDateClause:
            dateRange = 'where' + fromDateClause + ' and ' + toDateClause
        elif fromDateClause:
            dateRange = 'where' + fromDateClause
        elif toDateClause:
            dateRange = 'where' + toDateClause
        return dateRange

    def getAllAccountData(self, fromDate='', toDate=''):
        return self._ddbb.getData(
            'account',
            self._accountData,
            self._getDateRange('datetook', fromDate,toDate),
            'order by datetook',
            )


    def getAllCostsData(self, fromDate='', toDate=''):
        return self._ddbb.getData(
            'costs',
            self._costsData,
            self._getDateRange('date', fromDate, toDate),
            'order by date',
            )
