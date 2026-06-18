from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.get("/")
def root():
    return {"message": "Crypto Analytics API Running"}


# -----------------------------
# BASIC TRADES ENDPOINT
# -----------------------------
@app.get("/trades")
def get_trades():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT trade_id, price, quantity, event_time
        FROM trades
        ORDER BY created_at DESC
        LIMIT 100
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "trade_id": r[0],
            "price": float(r[1]),
            "quantity": float(r[2]),
            "event_time": r[3],
        }
        for r in rows
    ]


# -----------------------------
# 1. STATS ENDPOINT
# -----------------------------
@app.get("/stats")
def get_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_trades,
            COALESCE(AVG(price), 0),
            COALESCE(MAX(price), 0),
            COALESCE(MIN(price), 0)
        FROM trades;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_trades": row[0],
        "avg_price": float(row[1]),
        "max_price": float(row[2]),
        "min_price": float(row[3]),
    }


# -----------------------------
# 2. VOLUME ENDPOINT
# -----------------------------
@app.get("/volume")
def get_volume():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM trades;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_volume": float(row[0])
    }


# -----------------------------
# 3. LATEST PRICE ENDPOINT
# -----------------------------
@app.get("/latest-price")
def latest_price():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT price
        FROM trades
        ORDER BY event_time DESC
        LIMIT 1;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "latest_price": float(row[0]) if row else 0
    }
    