from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2
import os
import time
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
    for i in range(20):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "postgres"),
                port=int(os.getenv("DB_PORT", 5432)),
                database=os.getenv("DB_NAME", "crypto"),
                user=os.getenv("DB_USER", "crypto"),
                password=os.getenv("DB_PASSWORD", "crypto")
            )
            return conn
        except Exception as e:
            print(f"DB not ready (attempt {i+1}/20):", e)
            time.sleep(2)

    raise Exception("Database connection failed after retries")


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
    
#-----------------------------
# 4. PNL ENDPOINT
#-----------------------------
   
@app.get("/pnl")
def pnl():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            price,
            quantity
        FROM trades
        ORDER BY event_time DESC;
    """)

    rows = cur.fetchall()

    if not rows:
        return []

    # simple mock PnL logic (since no instrument mapping exists)
    avg_price = sum(r[0] for r in rows) / len(rows)

    total_qty = sum(r[1] for r in rows)

    last_price = rows[0][0]

    pnl_value = (last_price - avg_price) * total_qty

    return {
        "total_trades": len(rows),
        "avg_price": avg_price,
        "last_price": last_price,
        "total_quantity": total_qty,
        "pnl": pnl_value
    }
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.instrument,
            SUM(t.quantity) as qty,
            AVG(t.price) as avg_price,
            MAX(t.price) as last_price
        FROM trades t
        GROUP BY t.instrument;
    """)

    rows = cur.fetchall()

    result = []

    for r in rows:
        qty = float(r[1])
        avg = float(r[2])
        last = float(r[3])

        pnl = (last - avg) * qty

        result.append({
            "instrument": r[0],
            "quantity": qty,
            "avg_price": avg,
            "last_price": last,
            "pnl": pnl
        })

    return result