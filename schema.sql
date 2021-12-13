DROP TABLE IF EXISTS stocks_log;

CREATE TABLE stocks_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investment VARCHAR(10) NOT NULL,
    date_entered TIMESTAMP,
    shares INTEGER,
    entry DECIMAL(8,2),
    stop DECIMAL(8,2),
    target DECIMAL(8,2),
    exit DECIMAL(8,2),
    exit_date TIMESTAMP,
    notes TEXT,
    chart_url VARCHAR(255)
);
