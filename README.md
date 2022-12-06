# Introduction

# Requirements
```
apt get install sqlite3 python3
pip install -r requirements.txt
```


# Data feed
Define a path where the xls are present:

`export XLS_PATH=<path>`

Convert the xls to csv:

`./process-xls.sh $XLS_PATH`

Load the csv account data into the database:

`python3 csvloader.py -a $XLS_PATH/csv/`

Load the csv costs data into the database:

`python3 csvloader.py -c $XLS_PATH/csv/`

# SQLite3 read date values
Account:

`select date(datetook), * from account`
Costs:

`select date(date), * from costs`
