import socket
import time
import json
import random

HOST = "0.0.0.0"
PORT = 1337

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("AMD running on 1337...")

conn, addr = server.accept()
print("Client connected:", addr)

while True:
    trade = {
        "type": "trade",
        "data": {
            "trade_id": random.randint(1000, 9999),
            "instrument_id": "BTC",
            "price": round(random.uniform(60000, 65000), 2),
            "quantity": round(random.uniform(0.01, 2), 4),
            "side": random.choice(["BUY", "SELL"]),
            "date": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
    }

    conn.send((json.dumps(trade) + "\n").encode())
    time.sleep(1)