CREATE TABLE IF NOT EXISTS trades (
    trade_id BIGINT PRIMARY KEY,
    price NUMERIC(18,8),
    quantity NUMERIC(18,8),
    event_time BIGINT,
    created_at TIMESTAMP DEFAULT NOW()
);
