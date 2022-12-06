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
