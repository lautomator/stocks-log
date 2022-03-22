# Stocks Log

Keep track of your investments, including risk, profit, and loss. The app generates an overall report with some basic metrics including, frequency of trades, PnL, and trading patterns. There is the option to include a chart with each trade record.

This version of the app is intended as a demonstration of its features. I've included several fictional trades. This is not meant for the public or to be used in any way. A more robust version would have user accounts and a larger infastrcuture to include an entire administrative panel.

## Development

### Requirements
This is a [Flask](https://flask.palletsprojects.com/en/2.0.x/) Application that uses the Jinja templating system . You will need the following to do any development:

* click
* Flask
* itsdangerous
* Jinja2
* MarkupSafe
* Werkzeug

See `requirements.txt` for specific versions of each. You can create a virtual environment for this and install the requirements via Pip and Venv. Once you have that set up, you can use `start.sh` to run the environment. See the next section.

### Running the App Locally for Development
To start the virtual environment and get the server running:

* `sh start.sh`

* Navigate to `http://127.0.0.1:5000/` in the browser.

To stop the server and the virtual environment:

* `CTRL+C`

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

### Styles and SASS
```
>> cd static
>> sass --watch style.scss style.css
```

You can also use the `sass-watch.sh` script to watch for changes and update the loaded stylesheets.

## References

[Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
[Jinja Templates](https://jinja.palletsprojects.com/en/3.0.x/templates/)
[SQLite](https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/)
