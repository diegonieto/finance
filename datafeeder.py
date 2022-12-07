import logging
from ddbbfeeder import DatabaseFeeder
import getopt
import sys

if __name__ == "__main__":
    # Force=True because it can be already defined: 
    # https://stackoverflow.com/questions/20240464/python-logging-file-is-not-working-when-using-logging-basicconfig
    logging.basicConfig(filename='csvloader.log', 
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True,
                        level=logging.DEBUG)

    dataFeeder = DatabaseFeeder()

    opts, args = getopt.getopt(sys.argv[1:], "h:c:a:", ["accountpath=","costspath="])
    costspath = ''
    accountpath = ''
    for opt, arg in opts:
        if opt == '-h':
            print(__file__ + '-c <costs path> -a <account path>')
            exit()
        elif opt in ("-c", "--costspath"):
            costspath = arg
        elif opt in ("-a", "--accountpath"):
            accountpath = arg

    if accountpath:
        dataFeeder.importDataFromDirectory(accountpath, 'account')
    if costspath:
        dataFeeder.importDataFromDirectory(costspath, 'costs')
