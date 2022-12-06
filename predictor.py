from datamodel import DataContainer

import numpy

class DataPredictor(DataContainer):
    _trainModel = None
    _scaler = None

    _settings = None

    _isNormalized = False
    _isTrained = False


    def __init__(self, settings = {}) -> None:
        self._settings = settings

        self._isNormalized = True if self._settings['isNormalized'] else False
        super().__init__()


    def _normalizeData(self, dataToNormalize):
        self._logger.info('Normalizing data')
        self._logger.debug('Data: ' + str(dataToNormalize))
        dataToScale = numpy.array(dataToNormalize).reshape(-1,1)
        self._scaler.fit(dataToScale)
        dataNormalized = self._scaler.transform(dataToScale)
        self._logger.debug('Data Normalized: ' + str(dataNormalized))
        return dataNormalized


    def _normalize(self):
        if not self._isNormalized:
            for feature in self._data:
                self._logger.info('Normalizing feature: ' + feature)
                self._data[feature] = self._normalizeData(self._data[feature])

        self._isNormalized = True


    def train(self):
        if self._isTrained:
            return
        if not self._isDataSet:
            raise Exception('Data not set')
        if not self._isModelSet:
            raise Exception('Model not set')

        if not self._isNormalized:
            self._normalize()

        self._trainInternal()
        self._isTrained = True


    def predict(self, dataToPredict, isNormalized=False):
        if not self._isDataSet:
            raise Exception('Data not set')
        if not self._isModelSet:
            raise Exception('Model not set')
        if not self._isTrained:
            raise Exception('Not trained')

        if isNormalized:
            return self._predictInternal(dataToPredict)

        self._logger.debug('Data to predict: ' + str(dataToPredict))
        dataToPredictNormalized = self._scaler.transform(numpy.array(dataToPredict).reshape(-1,1))
        prediction = self._predictInternal(dataToPredictNormalized)
        self._logger.debug('Prediction normalized: ' + str(prediction))
        predictionDenormalized = self._scaler.inverse_transform(prediction)

        return predictionDenormalized


if __name__ == '__main__':
    dp = DataPredictor()
