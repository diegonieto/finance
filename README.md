# Introduction

# Requirements
```
apt get install sqlite3 python3
pip install -r requirements.txt
```


# Data feed
Define a path where the xls are present:

```
export XLS_PATH=<path>
export TMP_PATH=<path>
```

Convert the xls to csv:

`./process-xls.sh $XLS_PATH $TMP_PATH`

Load the csv account data into the database:

`python3 datafeeder.py -a $TMP_PATH`

Load the csv costs data into the database:

`python3 datafeeder.py -c $TMP_PATH`

# SQLite3 read date values
Account:

`select date(datetook), * from account`
Costs:

`select date(date), * from costs`
