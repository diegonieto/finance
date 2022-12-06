from ddbbfeeder import DatabaseFeeder
import logging
import getopt
import sys

if __name__ == "__main__":
    dataFeeder = DatabaseFeeder()

    # Force=True because it can be already defined: 
    # https://stackoverflow.com/questions/20240464/python-logging-file-is-not-working-when-using-logging-basicconfig
    logging.basicConfig(filename='csvloader.log', filemode='w',  force=True, level=logging.ERROR)

    opts, args = getopt.getopt(sys.argv[1:], "hca:", ["accountpath=","costspath="])
    costspath = ''
    accountpath = ''
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + '-c <costs path> -a <account path>')
            exit()
        elif opt in ("-c", "--costsdata"):
            costspath = arg
        elif opt in ("-a", "--accountdata"):
            accountpath = arg

    # TODO remove files with git filterbranch
    if (not ''):
        inputfile = '/home/dnieto/Documentos/personal/gastos/original/movimientos-agosto.csv'

    # dataFeeder.feedMovementsWithFileDb('/home/dnieto/Documentos/personal/gastos/original/movimientos-agosto.csv')

    if accountpath:
        dataFeeder.importDataFromDirectory(accountpath, 'account')
    if costspath:
        dataFeeder.importDataFromDirectory(costspath, 'costs')
