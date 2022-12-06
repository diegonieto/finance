import matplotlib.pyplot as plt

class DataPloter():
    _fig = None
    _ax1 = None

    def __init__(self) -> None:
        self._fig, self._ax1 = plt.subplots(num="Forecast")
        pass

    def plotData(self, x, y):
        # ax1.set_xticks(numpy.arange(len(x_train_date)))
        # ax1.set_xticklabels(x_train_date)

        # ax1.set_xticklabels(new_labels)
        # ax1.set_xticklabels(date, rotation=45) #rotate labels 45 degrees

        # ax1.set_xticks(numpy.arange(3), ['Tom', 'Dick', 'Sue'])  # Set text labels.
        # ax1.margins(x=0)

        # plt.xlim(0, 6)
        # plt.xlim(0, 6)

        self._ax1.scatter(x, y, color='blue')


    def plotForecast(self, x, y):
        self._ax1.plot(x, y, color='red')
        self._fig.savefig('output/account.png')
        plt.show()
