DROP TABLE IF EXISTS account_info;
DROP TABLE IF EXISTS stocks_log;

CREATE TABLE account_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_value FLOAT NOT NULL,
    maximum_risk INTEGER NOT NULL
);

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
    chart_url VARCHAR(255)
);
