import json
import ssl
import os
import time

from websocket import WebSocketApp
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# ------------------------
# DB CONNECTION (SAFE)
# ------------------------

def get_conn():
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "postgres"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "crypto"),
                user=os.getenv("DB_USER", "crypto"),
                password=os.getenv("DB_PASSWORD", "crypto")
            )
            print("✅ Connected to PostgreSQL")
            return conn
        except Exception as e:
            print(f"⏳ DB not ready ({i+1}/30):", e)
            time.sleep(2)

    raise Exception("DB connection failed")

# ------------------------
# INIT DB
# ------------------------

conn = get_conn()
cur = conn.cursor()

# ------------------------
# WEBSOCKET CALLBACKS
# ------------------------

def on_open(ws):
    print("Connected to stream ✔")

def on_message(ws, message):
    global conn, cur

    try:
        data = json.loads(message)

        trade_id = data["t"]
        price = float(data["p"])
        quantity = float(data["q"])
        event_time = data["E"]

        print(f"Price: {price} | Qty: {quantity} | ID: {trade_id}")

        cur.execute("""
            INSERT INTO trades (trade_id, price, quantity, event_time)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (trade_id) DO NOTHING
        """, (trade_id, price, quantity, event_time))

        conn.commit()

    except Exception as e:
        print("DB ERROR:", e)
        conn.rollback()

        # try reconnect once if broken
        try:
            conn = get_conn()
            cur = conn.cursor()
        except:
            pass

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection Closed")

# ------------------------
# WEBSOCKET STREAM
# ------------------------

socket_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

ws = WebSocketApp(
    socket_url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever(
    sslopt={"cert_reqs": ssl.CERT_NONE}
)