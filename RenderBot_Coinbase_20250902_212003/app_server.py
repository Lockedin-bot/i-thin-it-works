import os, threading, http.server, socketserver, json, csv
from run_paper import main as bot_main

PORT = int(os.environ.get("PORT", "10000"))
LOG_DIR = os.path.join(os.getcwd(), "logs")
HB_PATH = os.path.join(LOG_DIR, "heartbeat.log")
PRICES_PATH = os.path.join(LOG_DIR, "prices.csv")
TRADES_PATH = os.path.join(LOG_DIR, "trades.csv")

def start_bot():
    bot_main()  # blocks forever

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health", "/_health"):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok"); return
        if self.path == "/status":
            os.makedirs(LOG_DIR, exist_ok=True)
            status = {"heartbeat_tail": [], "last_prices": [], "last_trades": []}
            try:
                with open(HB_PATH, "r", encoding="utf-8") as f:
                    status["heartbeat_tail"] = [ln.strip() for ln in f.readlines()[-20:]]
            except Exception:
                pass
            try:
                rows = []
                with open(PRICES_PATH, "r", encoding="utf-8") as f:
                    for row in csv.reader(f): rows.append(row)
                status["last_prices"] = rows[-10:]
            except Exception:
                pass
            try:
                rows = []
                with open(TRADES_PATH, "r", encoding="utf-8") as f:
                    for row in csv.reader(f): rows.append(row)
                status["last_trades"] = rows[-10:]
            except Exception:
                pass
            body = json.dumps(status).encode()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body); return
        return super().do_GET()

if __name__ == "__main__":
    t = threading.Thread(target=start_bot, daemon=True); t.start()
    os.makedirs(LOG_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP server listening on :{PORT} (bot running in background)")
        httpd.serve_forever()
