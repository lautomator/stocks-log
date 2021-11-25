DROP TABLE IF EXISTS stocks_log;

CREATE TABLE stocks_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investment VARCHAR(10) NOT NULL,
    date_entered TIMESTAMP NOT NULL,
    shares INTEGER NOT NULL,
    entry FLOAT NOT NULL,
    stop FLOAT NOT NULL,
    target FLOAT NOT NULL,
    risk_share FLOAT NOT NULL,
    exit FLOAT NOT NULL,
    sell_date TIMESTAMP NOT NULL,
    pnl FLOAT NOT NULL,
    notes TEXT NOT NULL,
    chart_url VARCHAR(255) NOT NULL
);
