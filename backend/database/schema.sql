CREATE TABLE users (
    user_id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

INSERT INTO users VALUES ('admin', 'bank', '555');

CREATE TABLE dashboards (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    paper_id VARCHAR NOT NULL,
    paper_info JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE papers (
    id VARCHAR PRIMARY KEY,
    paper_id VARCHAR NOT NULL,
    note_id VARCHAR NOT NULL,
    page VARCHAR,
    tags JSON,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
