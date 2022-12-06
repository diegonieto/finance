#!/bin/bash

if [ -z $1 ]; then
    echo "Missing path to process xls files"
fi

XLS_FILES_PATH=$1

mkdir -p ${XLS_FILES_PATH}/csv
for file in `ls ${XLS_FILES_PATH}/*.xls`; do
    echo "Processing $file"
    NAME_WITHOUT_EXTENSION=${file:0:$((${#file}-3))}
    CSV_FILE=${NAME_WITHOUT_EXTENSION}csv
    if [ ! -f "csv/${CSV_FILE}" ]; then
        echo "Converting"
        # libreoffice --convert-to csv $file
        python3 xlstocsv.py $file
        mv ${CSV_FILE} ${XLS_FILES_PATH}/csv
    fi
done
