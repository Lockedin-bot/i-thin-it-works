import json
import gspread
from google.oauth2.service_account import Credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
class SheetsLogger:
    def __init__(self, service_account_json: str, spreadsheet_id: str):
        if not service_account_json or not spreadsheet_id:
            raise ValueError("SheetsLogger requires GOOGLE_SERVICE_ACCOUNT_JSON and SPREADSHEET_ID")
        info = json.loads(service_account_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        self.gc = gspread.authorize(creds)
        self.spreadsheet = self.gc.open_by_key(spreadsheet_id)
        self._ensure_ws("trades", ["timestamp","symbol","side","price","units","equity_after"])
        self._ensure_ws("equity_curve", ["timestamp","equity"])
    def _ensure_ws(self, title, headers):
        try:
            ws = self.spreadsheet.worksheet(title)
        except gspread.exceptions.WorksheetNotFound:
            ws = self.spreadsheet.add_worksheet(title=title, rows=1000, cols=len(headers))
            ws.append_row(headers, value_input_option="RAW")
        return ws
    def append_trade(self, row: dict):
        self.spreadsheet.worksheet("trades").append_row(
            [row.get("timestamp",""), row.get("symbol",""), row.get("side",""),
             row.get("price",""), row.get("units",""), row.get("equity_after","")],
            value_input_option="USER_ENTERED"
        )
    def append_equity_point(self, timestamp: str, equity: float):
        self.spreadsheet.worksheet("equity_curve").append_row([timestamp, equity], value_input_option="USER_ENTERED")
