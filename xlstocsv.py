import pandas as pd
import sys
import os

if sys.argv is None:
    print('Excel file not provided')

if len(sys.argv) != 2:
    print('Invalid number of parameters')

file = sys.argv[1]

print('File ' + file + ' ready to read')
readObject = pd.read_excel (file)

basename = os.path.basename(file)
basenameWithoutExtension = os.path.splitext(basename)[0]
newFilename = os.path.join(os.path.dirname(file), basenameWithoutExtension)
newFilename += '.csv'

print('File ' + newFilename + ' ready to write')

# Write the dataframe object
# into csv file
readObject.to_csv (newFilename,
    index = None,
    header=True)
