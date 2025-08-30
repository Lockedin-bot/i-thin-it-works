import os, time, csv
import pandas as pd
from datetime import datetime, timezone
from core.utils import load_settings, setup_logger, parse_symbols
from data.marketdata import fetch_ohlcv
from strategies.momentum import momentum_signals
from core.risk import position_size

def main():
    s = load_settings()
    log = setup_logger(s.LOG_LEVEL)
    os.makedirs("logs", exist_ok=True)
    trades_path, hb_path = "logs/trades.csv", "logs/heartbeat.log"
    if not os.path.exists(trades_path):
        with open(trades_path, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp","symbol","side","price","units","equity_after"])
    symbols = parse_symbols(s.SYMBOLS)
    if not symbols: log.error("No symbols configured. Set SYMBOLS=... in your .env"); return
    equity = {sym: s.TOTAL_EQUITY / len(symbols) for sym in symbols}
    position = {sym: 0 for sym in symbols}
    tf_map = {"1m":60, "5m":300, "15m":900, "1h":3600}; gran = tf_map.get(s.TA_TIMEFRAME, 300)
    log.info(f"Starting multi-coin paper bot | SYMS={symbols} TF={s.TA_TIMEFRAME} FAST={s.FAST_MA} SLOW={s.SLOW_MA}")
    while True:
        try:
            for sym in symbols:
                df = fetch_ohlcv(symbol=sym, granularity=gran)
                if df is None or len(df) < max(s.FAST_MA, s.SLOW_MA) + 2:
                    msg = f"HEARTBEAT {sym} insufficient data"
                    print(msg, flush=True)
                    with open(hb_path, "a", encoding="utf-8") as hb: hb.write(f"{datetime.now(timezone.utc).isoformat()} {msg}\n")
                    continue
                df = momentum_signals(df, fast=s.FAST_MA, slow=s.SLOW_MA); last = df.iloc[-1]
                price = float(last["close"]); signal = int(last["signal"]) if pd.notna(last["signal"]) else 0
                msg = f"HEARTBEAT {sym} price={price:.4f} signal={signal} pos={position[sym]} equity={equity[sym]:.2f}"
                log.info(msg); print(msg, flush=True)
                with open(hb_path, "a", encoding="utf-8") as hb: hb.write(f"{datetime.now(timezone.utc).isoformat()} {msg}\n")
                if signal == 1 and position[sym] <= 0:
                    units = 1; cost = units * price
                    if cost <= equity[sym]:
                        equity[sym] -= cost; position[sym] += units
                        trade_msg = f"TRADE {sym} BUY {units} @ {price:.4f} | equity={equity[sym]:.2f}"
                        log.info(trade_msg); print(trade_msg, flush=True)
                        with open(trades_path, "a", newline="") as f:
                            csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), sym, "BUY", price, units, equity[sym]])
                elif signal == -1 and position[sym] > 0:
                    proceeds = position[sym] * price; equity[sym] += proceeds
                    trade_msg = f"TRADE {sym} SELL {position[sym]} @ {price:.4f} | equity={equity[sym]:.2f}"
                    log.info(trade_msg); print(trade_msg, flush=True)
                    with open(trades_path, "a", newline="") as f:
                        csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), sym, "SELL", price, position[sym], equity[sym]])
                    position[sym] = 0
            time.sleep(30)
        except Exception as e:
            log.exception(e); print(f"ERROR: {e}", flush=True); time.sleep(10)

if __name__ == "__main__": main()
