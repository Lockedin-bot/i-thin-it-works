import os, threading, http.server, socketserver, json, csv
from run_paper import main as bot_main
PORT = int(os.environ.get("PORT", "10000"))
def start_bot(): bot_main()
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health", "/_health"):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok"); return
        if self.path.startswith("/status"):
            status = {}
            try:
                with open("logs/heartbeat.log","r",encoding="utf-8") as f:
                    status["heartbeat_tail"] = [ln.strip() for ln in f.readlines()[-20:]]
            except Exception: status["heartbeat_tail"] = []
            try:
                rows = []
                with open("logs/trades.csv","r",newline="") as f:
                    for row in csv.reader(f): rows.append(row)
                status["trades_last"] = rows[-10:]
            except Exception: status["trades_last"] = []
            body = json.dumps(status).encode()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(body); return
        return super().doGET()
if __name__ == "__main__":
    t = threading.Thread(target=start_bot, daemon=True); t.start()
    os.makedirs("logs", exist_ok=True)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP server listening on :{PORT} (bot running in background)")
        httpd.serve_forever()
