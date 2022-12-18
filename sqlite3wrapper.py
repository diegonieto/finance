import sqlite3
import logging

class SQLite3Wrapper:
    _con = None
    _cursor = None
    _logger = None

    def __init__(self, databasePath) -> None:
        self._con = sqlite3.connect(databasePath)
        self._cursor = self._con.cursor()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)

    def createTable(self, table):
        try:
            self._cursor.execute('CREATE TABLE ' + table)
        except:
            self._logger.warning('table already exists')

    def getData(self, table, fields='*', condition='', order=''):
        res = self._cursor.execute('SELECT ' + fields + ' FROM ' + table  + ' ' + condition + ' ' + order)
        return res.fetchall()

    def insertData(self, table, values):
        self._logger.debug('adding ' + values + ' to table ' + table)
        query = 'INSERT INTO ' + table + ' VALUES (' + values + ')'
        try:
            self._cursor.execute(query)
            self._con.commit()
        except Exception as Argument:
            self._logger.error('Error when inserting the data: ' + query)

    def createIndex(self, table, index):
        query = 'CREATE INDEX ' + table + '_index' + ' ON ' + table + ' (' + index + ')'
        try:
            self._cursor.execute(query)
        except:
            self._logger.error('Query error: ' + query)
