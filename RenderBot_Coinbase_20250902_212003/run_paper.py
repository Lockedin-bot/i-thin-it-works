import os, csv, time
from datetime import datetime, timezone
import pandas as pd

from core.utils import load_env, setup_logger, parse_symbols
from data.marketdata import fetch_ohlcv
from strategies.momentum import momentum_signals

LOG_DIR = os.path.join(os.getcwd(), "logs")
HB_PATH = os.path.join(LOG_DIR, "heartbeat.log")
PRICES_PATH = os.path.join(LOG_DIR, "prices.csv")
TRADES_PATH = os.path.join(LOG_DIR, "trades.csv")

def ensure_files():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(PRICES_PATH):
        with open(PRICES_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["timestamp","symbol","close","fast_ma","slow_ma","signal"])
    if not os.path.exists(TRADES_PATH):
        with open(TRADES_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["timestamp","symbol","side","price","units","note"])

def log_heartbeat(msg:str):
    print(msg, flush=True)
    try:
        with open(HB_PATH, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

def main():
    env = load_env()
    log = setup_logger(env["LOG_LEVEL"])
    symbols = parse_symbols(env["SYMBOLS"])
    timeframe = env["TA_TIMEFRAME"]
    fast = env["FAST_MA"]; slow = env["SLOW_MA"]
    loop_sec = env["LOOP_SEC"]

    ensure_files()
    log.info(f"Starting (Coinbase) | syms={symbols} tf={timeframe} fast={fast} slow={slow} loop={loop_sec}s")

    # simple paper position dict
    pos = {s: 0 for s in symbols}

    while True:
        try:
            for sym in symbols:
                df = fetch_ohlcv(sym, timeframe, limit=max(slow+5, 120))
                if df is None or len(df) < max(fast, slow) + 2:
                    log_heartbeat(f"HEARTBEAT {sym} insufficient data")
                    continue
                df = momentum_signals(df, fast=fast, slow=slow)
                last = df.iloc[-1]
                close = float(last["close"])
                fast_ma = float(last["fast"]) if pd.notna(last["fast"]) else None
                slow_ma = float(last["slow"]) if pd.notna(last["slow"]) else None
                signal = int(last["signal"]) if pd.notna(last["signal"]) else 0

                # Write price row
                with open(PRICES_PATH, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), sym, close, fast_ma, slow_ma, signal])

                # very simple paper trade: 1 unit on cross
                if signal == 1 and pos[sym] <= 0:
                    pos[sym] += 1
                    with open(TRADES_PATH, "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), sym, "BUY", close, 1, "fast>slow"])
                elif signal == -1 and pos[sym] > 0:
                    with open(TRADES_PATH, "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerow([datetime.now(timezone.utc).isoformat(), sym, "SELL", close, pos[sym], "fast<slow"])
                    pos[sym] = 0

                log_heartbeat(f"HEARTBEAT {sym} close={close:.4f} fast={fast_ma} slow={slow_ma} signal={signal} pos={pos[sym]}")
            time.sleep(loop_sec)
        except Exception as e:
            import traceback; traceback.print_exc(); time.sleep(10)

if __name__ == "__main__":
    main()
