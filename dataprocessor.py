from ddbbreader import DatabaseReader
from linearPredictor import LinearDataPredictor
from dataploter import DataPloter

import logging
import numpy
import getopt
import sys

if __name__ == "__main__":
    logging.basicConfig(filename='dataprocessor.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True,
                        level=logging.INFO)

    opts, args = getopt.getopt(sys.argv[1:], "h:f:", ["from="])
    fromDate = '2022-06-01'
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + '-f <date from look in "yyyy-mm-dd" format>')
            exit()
        elif opt in ("-f", "--from"):
            fromDate = arg


    # Read DDBB data
    dataReader = DatabaseReader()
    accountData = dataReader.getAllAccountData(fromDate=fromDate)
    print(accountData)

    # Choose ranges
    accountDataArray = numpy.array(accountData)
    if not accountDataArray.size:
        raise Exception('Empty values')

    x_train = accountDataArray[:,0]
    y_train = accountDataArray[:,3]

    x_train_date = list(map(dataReader.toDateformat, x_train))
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
    dataPlotter = DataPloter()
    dataPlotter.plotData(x_train_int, y_train_float)
    dataPlotter.plotForecast(x_pred_int, prediction)
