import os, json, sys
from datetime import datetime, timezone
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_env(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        print(f"ERROR: Missing environment variable: {name}")
        sys.exit(1)
    return val

def main():
    spreadsheet_id = get_env("SPREADSHEET_ID")
    sa_json_raw   = get_env("GOOGLE_SERVICE_ACCOUNT_JSON")
    info = json.loads(sa_json_raw)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)

    def ensure_ws(title, headers):
        try:
            ws = sh.worksheet(title)
        except gspread.exceptions.WorksheetNotFound:
            ws = sh.add_worksheet(title=title, rows=1000, cols=len(headers))
            ws.append_row(headers, value_input_option="RAW")
        return ws

    trades = ensure_ws("trades", ["timestamp","symbol","side","price","units","equity_after"])
    equity = ensure_ws("equity_curve", ["timestamp","equity"])

    ts = datetime.now(timezone.utc).isoformat()
    trades.append_row([ts, "TEST", "PING", "", "", ""], value_input_option="USER_ENTERED")
    equity.append_row([ts, 12345], value_input_option="USER_ENTERED")
    print("SUCCESS: wrote to Google Sheet.")

if __name__ == "__main__":
    main()
