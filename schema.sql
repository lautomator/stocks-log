DROP TABLE IF EXISTS stocks_log;

CREATE TABLE stocks_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investment VARCHAR(10) NOT NULL,
    date_entered TIMESTAMP,
    shares INTEGER,
    entry FLOAT,
    stop FLOAT,
    target FLOAT,
    risk_share FLOAT,
    exit FLOAT,
    sell_date TIMESTAMP,
    pnl FLOAT,
    notes TEXT,
    chart_url VARCHAR(255)
);
