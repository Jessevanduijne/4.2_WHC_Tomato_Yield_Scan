DROP TABLE IF EXISTS results;

CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_id TEXT,
    session_id TEXT,
    files_dtype TEXT,
    files BLOB,
    val BLOB,
    percent_healthy REAL,
    result_date TIMESTAMP
);