import json
import ssl
import os

from websocket import WebSocketApp
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# ------------------------
# DATABASE CONNECTION
# ------------------------

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "crypto"),
    user=os.getenv("DB_USER", "crypto"),
    password=os.getenv("DB_PASSWORD", "crypto")
)

cur = conn.cursor()

print("Connected to PostgreSQL ✔")

# ------------------------
# WEBSOCKET CALLBACKS
# ------------------------

def on_open(ws):
    print("Connected to Binance ✔")


def on_message(ws, message):
    try:
        data = json.loads(message)

        trade_id = data["t"]
        price = float(data["p"])
        quantity = float(data["q"])
        event_time = data["E"]

        print(
            f"Price: {price} | "
            f"Quantity: {quantity} | "
            f"Trade ID: {trade_id}"
        )

        cur.execute(
            """
            INSERT INTO trades (
                trade_id,
                price,
                quantity,
                event_time
            )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (trade_id)
            DO NOTHING
            """,
            (
                trade_id,
                price,
                quantity,
                event_time
            )
        )

        conn.commit()

        print(f"Inserted Trade: {trade_id}")

    except Exception as e:
        print("DB ERROR:", e)
        conn.rollback()


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Connection Closed")


# ------------------------
# BINANCE WEBSOCKET
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