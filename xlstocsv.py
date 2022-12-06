import pandas as pd
import sys
import os

if sys.argv is None:
    print('Excel file not provided')

destPath = None
if len(sys.argv) == 3:
    destPath = sys.argv[2]

file = sys.argv[1]

print('File ' + file + ' ready to read')
readObject = pd.read_excel (file)

basename = os.path.basename(file)
basenameWithoutExtension = os.path.splitext(basename)[0]
if destPath is None:
    newFilename = os.path.join(os.path.dirname(file), basenameWithoutExtension)
else:
    newFilename = os.path.join(destPath, basenameWithoutExtension)
newFilename += '.csv'

print('File ' + newFilename + ' ready to write')

# Write the dataframe object
# into csv file
readObject.to_csv (newFilename,
    index = None,
    header=True)
