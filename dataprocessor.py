from ddbbreader import DatabaseReader
from linearPredictor import LinearDataPredictor
from clusterpredictor import ClusterDataPredictor
from dataplotter import DataPlotter

import logging
import numpy
import getopt
import sys
import datetime
from dateutil.relativedelta import relativedelta

def processAccount(dataReader, settings):
    fromDate = settings['fromDate']
    toDate = settings['toDate']

    # Read DDBB data
    accountData = dataReader.getAllAccountData(fromDate=fromDate, toDate=toDate)

    # Choose ranges
    accountDataArray = numpy.array(accountData)
    if not accountDataArray.size:
        raise Exception('Empty values')

    x_train = accountDataArray[:,0]
    y_train = accountDataArray[:,3]

    x_train_int = list(map(int, x_train))
    y_train_float = list(map(float, y_train))

    # Make predictions
    Normalized = True

    dp = LinearDataPredictor({'isNormalized' : Normalized})
    dp.setModel(dp.getDefaultModel())
    dp.setData({
        'x' : numpy.array(x_train_int),
        'y' : numpy.array(y_train_float),
    })
    dp.train()
    dates_to_pred = [
        "2023-01-01",
        "2023-04-01",
        "2023-07-01",
        "2023-10-01",
        "2024-01-01"
    ]
    x_pred = [dataReader.toEpoch(date) for date in dates_to_pred]
    x_pred_int = list(map(int, x_pred))

    prediction = dp.predict(numpy.array(x_pred_int), Normalized)

    # Plot data
    dataPlotter = DataPlotter()
    dataPlotter.plotData(x_train_int, y_train_float)
    dataPlotter.plotForecast(x_pred_int, prediction)
    dataPlotter.showAccount()


def processCosts(dataReader, clusters, settings):
    fromDate = settings['fromDate']
    toDate = settings['toDate']

    # Read DDBB costs
    costsData = dataReader.getAllCostsData(fromDate=fromDate, toDate=toDate)
    costsDataArray = numpy.array(costsData)

    if not costsDataArray.size:
        logging.warning('Not enough data')
        return

    x_train = costsDataArray[:,2]

    clusters = min(clusters, x_train.size)
    Normalized = True
    dp = ClusterDataPredictor({
        'isNormalized' : Normalized,
        'clusters' : clusters
    })
    dp.setModel(dp.getDefaultModel())
    dp.setData({
        'x' : x_train,
    })
    dp.train()

    dataPlotter = DataPlotter(settings)
    dataPlotter.plotCluster(dp.getCenters())


if __name__ == "__main__":
    logging.basicConfig(filename='dataprocessor.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True,
                        level=logging.INFO)

    opts, args = getopt.getopt(sys.argv[1:], "h:f:t:c:r:", ["from=", "to=", "clusters=", "report="])
    fromDate = '2022-06-01'
    toDate = '2023-06-01'
    nlastMonths = 6
    clusters = 10

    for opt, arg in opts:
        if opt == '-h':
            print(__file__
            + ' -f <date from look in "yyyy-mm-dd" format>'
            + ' -t <date from look in "yyyy-mm-dd" format>>'
            + ' -c <number of clusters to generate the costs graph>'
            + ' -r <number of last months to generate the report>'
            )
            exit()
        elif opt in ("-f", "--from"):
            fromDate = arg
        elif opt in ("-c", "--clusters"):
            clusters = arg
        elif opt in ("-to", "--to"):
            toDate = arg
        elif opt in ("-r", "--report"):
            nlastMonths = arg

    dataReader = DatabaseReader()
    settings = {
        'fromDate' : fromDate,
        'toDate' : toDate,
    }
    processCosts(dataReader, clusters, settings)
    processAccount(dataReader, settings)

    current = datetime.date.today()
    oneMonthBeforeCurrent = None
    for month in numpy.arange(nlastMonths, dtype=int):
        oneMonthBeforeCurrent = current - relativedelta(months=1)
        settings = {
            'fromDate' : str(oneMonthBeforeCurrent),
            'toDate' : str(current),
            'plot' : True,
        }
        processCosts(dataReader, clusters, settings)
        current = oneMonthBeforeCurrent
