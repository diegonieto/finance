import matplotlib.pyplot as plt
import os
import numpy

class DataPloter():
    _figAccount = None
    _ax1Account = None
    _figCosts = None
    _ax1Costs = None
    _settings = None
    _plot = True

    def __init__(self, settings = None) -> None:
        self._settings = settings
        if settings and 'plot' in settings:
            self._plot = settings['plot']

    def plotData(self, x, y):
        self._figAccount, self._ax1Account = plt.subplots(num="Forecast")
        # ax1.set_xticks(numpy.arange(len(x_train_date)))
        # ax1.set_xticklabels(x_train_date)

        # ax1.set_xticklabels(new_labels)
        # ax1.set_xticklabels(date, rotation=45) #rotate labels 45 degrees

        # ax1.set_xticks(numpy.arange(3), ['Tom', 'Dick', 'Sue'])  # Set text labels.
        # ax1.margins(x=0)

        # plt.xlim(0, 6)
        # plt.xlim(0, 6)

        self._ax1Account.scatter(x, y, color='blue')
        self._ax1Account.plot(x, y, color='grey')


    def plotForecast(self, x, y):
        if not os.path.exists('output'):
            os.mkdir('output')
        self._ax1Account.plot(x, y, color='red')
        self._figAccount.savefig('output/account.png')
        plt.show()


    def plotCluster(self, data):
        self._figCosts, self._ax1Costs = plt.subplots(num="Costs")
        self._ax1Costs.scatter(data, data, color="red", linewidth=2)
        # plt.xlim(0, 400)
        # plt.ylim(0, 400)

        suffix = ''
        if self._settings:
            suffix = '-'+self._settings['fromDate']+'-to-'+self._settings['toDate']

        self._figCosts.savefig('output/costs'+suffix+'.png')

        if self._plot:
            plt.show()
