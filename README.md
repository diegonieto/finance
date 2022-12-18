# Introduction
Finance is tool that helps with the own knowledge of the finance status. It basically tries to discover your account management. To do that two tools are provided:
* Datafeeder: To import the account balance and movements independently
* Dataprocessor: That process the imported data and generates a forecast based on its historic

The plots are saved in the img folder. Also, a Jenkinsfile is provided to automatize the data injection
by scanning a folder automatically.

The input data sopported is .xls or .csv files with the format shown in the example


# Requirements
```
apt get install sqlite3 python3
pip install -r requirements.txt
```

# Running the example
```
./process-xls.sh example /tmp/miau
python3 datafeeder.py -a /tmp/miau
python3 dataprocessor.py
```
<img title="Example forecast" alt="Example Forecast" src="img/example.png">


# Feeding with your own data
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

# Show data processed
Database should be filled before:

`python3 dataprocessor.py`

# SQLite3 read date values
Account:

`select date(datetook), * from account`
Costs:

`select date(date), * from costs`

# Check linear predictor for account

`python3 linearPredictor.py`
