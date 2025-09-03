# Coinbase Heartbeat Bot (Render-ready, persistent logs)

- Pulls OHLCV candles from **Coinbase Exchange** public API
- Computes simple **fast/slow MA** per symbol
- Logs heartbeats to \/app/logs/heartbeat.log\, last prices to \/app/logs/prices.csv\, and paper trades to \/app/logs/trades.csv\
- HTTP:
  - \/health\ → ok
  - \/status\ → last 20 heartbeats, last 10 prices + trades

## Local test (optional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
="INFO"; ="BTC-USD,ETH-USD,SOL-USD"; ="5m"; ="12"; ="26"; ="10"
python -u app_server.py
# open http://localhost:10000/status
