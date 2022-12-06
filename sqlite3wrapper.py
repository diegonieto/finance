import sqlite3
import logging

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
        res = self._cursor.execute('SELECT ' + fields + ' FROM ' + table  + ' ' + condition)
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
