DROP TABLE IF EXISTS stocks_log;

CREATE TABLE stocks_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investment VARCHAR(10) NOT NULL,
    date_entered TIMESTAMP,
    shares INTEGER,
    entry DECIMAL(8,2),
    stop DECIMAL(8,2),
    target DECIMAL(8,2),
    risk_share DECIMAL(8,2),
    exit DECIMAL(8,2),
    sell_date TIMESTAMP,
    pnl DECIMAL(8,2),
    notes TEXT,
    chart_url VARCHAR(255)
);
