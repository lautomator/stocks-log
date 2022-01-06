# Stocks Log

ref: https://flask.palletsprojects.com/en/2.0.x/
ref: https://jinja.palletsprojects.com/en/3.0.x/templates/

App is intended to run locally only. This is not meant for a server or the public.



## Running the App
To start the virtual environment and get the server running:

* `sh start.sh`

* Navigate to `http://127.0.0.1:5000/` in the browser.

To stop the server and the virtual environment:

* `CTRL+C`

## Database
ref: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

### SQLite3 Shell
Begin by running the virtual environment in the command line shell.

```
>> cd stocks
>> . env/bin/activate
>> sqlite3
sqlite> .open stocks.db
sqlite> select * from stocks_log;
sqlite> <your sql commands>
sqlite> .exit
```

Import a table:

```
>> cd stocks
>> . env/bin/activate
>> sqlite3
sqlite> .open stocks.db
sqlite> .schema
sqlite> .mode csv
sqlite> .import <path/to/csv/file> stocks_log
```

## Development
```
>> cd static
>> sass --watch style.scss style.css
```


