from websocket import WebSocketApp
import json
import ssl

# WebSocket URL for Binance BTC/USDT trades
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# Callback functions for WebSocket events
def on_message(ws, message):
    data = json.loads(message)

    print(
        f"Price: {data['p']} | "
        f"Quantity: {data['q']} | "
        f"Trade ID: {data['t']}"
    )
    
# Other callback functions for WebSocket events    
def on_error(ws, error):
    print(f"Error: {error}")
    
def on_close(ws, close_status_code, close_msg):
    print("Connection Closed")

def on_open(ws):
    print("Connected to Binance")
    
    
    
if __name__ == "__main__":
    ws = WebSocketApp(
        SOCKET,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # ws.run_forever()
    
    ws.run_forever(
    sslopt={"cert_reqs": ssl.CERT_NONE}
)