#!/bin/bash

if [ -z $1 ]; then
    echo "Missing path to process xls files"
fi

XLS_FILES_PATH=$1

declare DEST_PATH
if [ -z $2 ]; then
    echo "Missing path to process xls files"
    DEST_PATH="/tmp"
else
    DEST_PATH=$2
fi

mkdir -p ${DEST_PATH}
for FILE in `ls ${XLS_FILES_PATH}/*.xls`; do
    echo "Processing $file"
    NAME_WITHOUT_EXTENSION=${FILE:0:$((${#FILE}-3))}
    NAME_WITHOUT_EXTENSION=$(basename ${NAME_WITHOUT_EXTENSION})
    CSV_FILE=${NAME_WITHOUT_EXTENSION}csv
    echo "name without $CSV_FILE"
    if [ ! -f "${DEST_PATH}/${CSV_FILE}" ]; then
        echo "Converting"
        python3 xlstocsv.py ${FILE} "${DEST_PATH}"
    fi
done
