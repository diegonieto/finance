import logging

class DataContainer:
    _logger = None
    _isModelSet = False
    _isDataSet = False

    _defaultModel = {
        'inputs' : {
            'x' : 'Date',
        },
        'outputs' : {
            'y' : 'Balance'
        }
    }

    _model = _defaultModel
    _data = {
        'x' : [0, 1],
        'y' : [0, 2],
    }


    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)


    def getDefaultModel(self):
        return self._defaultModel


    def setModel(self, model):
        self._model = model
        self._logger.info('Model: ' + str(model))
        self._isModelSet = True


    def plotForecast(self, date):
        if not self._isModelSet:
            logging.error('Model was not set')
        if not self._isDataSet:
            logging.error('Data was not set')


    def setData(self, data):
        self._data = data
        self._isDataSet = True