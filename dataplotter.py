import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy

class DataPlotter():
    _figAccount = None
    _ax1Account = None
    _figCosts = None
    _ax1Costs = None
    _settings = None
    _plot = True

    def _initAccount(self):
        if self._figAccount is None:
            self._figAccount, self._ax1Account = plt.subplots(num="Forecast")


    def _initCosts(self):
        if self._figCosts is None:
            self._figCosts, self._ax1Costs = plt.subplots(num="Costs")


    def showAccount(self):
        # Account plot settings
        self._ax1Account.set_title('Balance forecast')
        self._ax1Account.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self._ax1Account.set_xlabel('Date')
        self._ax1Account.set_ylabel('€')
        self._ax1Account.legend(loc='upper center', shadow=True, fontsize='x-large')

        if not os.path.exists('output'):
            os.mkdir('output')
        self._figAccount.savefig('output/account.png')
        plt.show()


    def showCosts(self):
        # Costs plot settings
        self._ax1Costs.set_title('')
        suffix = ''
        if self._settings:
            suffix = '-'+self._settings['fromDate']+'-to-'+self._settings['toDate']
        self._ax1Costs.set_title('Costs ' + suffix)
        self._ax1Costs.set_xlabel('€')
        self._ax1Costs.set_ylabel('€')
        self._ax1Costs.legend(loc='upper center', shadow=True, fontsize='x-large')

        if not os.path.exists('output'):
            os.mkdir('output')
        self._figCosts.savefig('output/costs'+suffix+'.png')
        if self._plot:
            plt.show()


    def __init__(self, settings = None) -> None:
        self._settings = settings
        if settings and 'plot' in settings:
            self._plot = settings['plot']


    def plotData(self, x, y):
        self._initAccount()
        x = numpy.asarray(x, dtype='datetime64[s]')
        self._ax1Account.set_xticklabels(x, rotation=45)
        self._ax1Account.scatter(x, y, color='blue', label='historic data')


    def plotForecast(self, x, y):
        self._initAccount()
        x = numpy.asarray(x, dtype='datetime64[s]')
        self._ax1Account.set_xticklabels(x, rotation=20)
        self._ax1Account.plot(x, y, color='red', label='forecast')


    def plotCluster(self, data):
        self._initCosts()
        self._ax1Costs.clear()
        self._ax1Costs.set_ylim(-500, 500)
        self._ax1Costs.set_xlim(-500, 500)
        self._ax1Costs.scatter(data, data, color="red", marker='+', label='costs')
        self.showCosts()
