from predictor import DataPredictor

from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler

import logging
import numpy

import matplotlib.pyplot as plot

class LinearDataPredictor(DataPredictor):
    def __init__(self, settings = {}) -> None:
        super().__init__(settings)
        self._logger.info('Initializing')
        # Default training model
        self._trainModel = linear_model.LinearRegression()
        self._scaler = MinMaxScaler()


    def _trainInternal(self):
        inputMap = list(self._model['inputs'].keys())
        outputMap = list(self._model['outputs'].keys())

        self._logger.debug('input map: ' + str(inputMap[0]))
        self._logger.debug('output map: ' + str(outputMap[0]))

        intputData = self._data[inputMap[0]]
        outputData = self._data[outputMap[0]]

        self._logger.debug('data: ' + str(self._data))
        self._logger.debug('input data map: ' + str(intputData))
        self._logger.debug('output data map: ' + str(outputData))

        x = numpy.array(intputData).reshape(-1, 1)
        y = numpy.array(outputData).reshape(-1, 1)
        self._trainModel.fit(x, y)
        self._logger.debug('score: ' + str(self._trainModel.score(x, y)))


    def _predictInternal(self, dataToPredict):
        self._logger.debug('trying to predict: ' + str(dataToPredict))
        return self._trainModel.predict(numpy.array(dataToPredict).reshape(-1, 1))


if __name__ == '__main__':
    logging.basicConfig(filename=__file__+'.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True,
                        level=logging.DEBUG)

    logging.info('Starting')

    size = 50

    x = numpy.arange(size, dtype=int)
    y = numpy.square(x)

    Normalized = True

    dp = LinearDataPredictor({'isNormalized' : Normalized})
    dp.setModel(dp.getDefaultModel())
    dp.setData({
        'x' : x,
        'y' : y,
    })
    dp.train()

    prediction = dp.predict(x, Normalized)
    plot.scatter(x, y, color="blue")
    plot.plot(x, prediction, color="red", linewidth=2)
    plot.show()
