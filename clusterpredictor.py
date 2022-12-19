from predictor import DataPredictor

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

import logging
import numpy

import matplotlib.pyplot as plot

class ClusterDataPredictor(DataPredictor):
    def __init__(self, settings = {}) -> None:
        super().__init__(settings)
        self._logger.info('Initializing')
        # Default training model
        clusters = settings['clusters']
        self._trainModel = KMeans(n_clusters=int(clusters))
        self._scaler = MinMaxScaler()


    def _trainInternal(self):
        inputMap = list(self._model['inputs'].keys())

        self._logger.debug('input map: ' + str(inputMap[0]))

        intputData = self._data[inputMap[0]]

        self._logger.debug('data: ' + str(self._data))
        self._logger.debug('input data map: ' + str(intputData))

        x = numpy.array(intputData).reshape(-1, 1)
        self._trainModel.fit(x)


    def _predictInternal(self, dataToPredict):
        self._logger.debug('trying to predict: ' + str(dataToPredict))
        return self._trainModel.predict(numpy.array(dataToPredict).reshape(-1, 1))


    def getCenters(self):
        return self._trainModel.cluster_centers_

if __name__ == '__main__':
    logging.basicConfig(filename=__file__+'.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True,
                        level=logging.DEBUG)

    logging.info('Starting')

    x = numpy.array([1, 1, 1, 4, 5, 5, 6, 9, 9, 9])

    Normalized = True

    dp = ClusterDataPredictor({'isNormalized' : Normalized})
    dp.setModel(dp.getDefaultModel())
    dp.setData({
        'x' : x,
    })
    dp.train()

    print(dp.getCenters())

    plot.scatter(dp.getCenters(), dp.getCenters(), color="red", linewidth=2)
    plot.show()
