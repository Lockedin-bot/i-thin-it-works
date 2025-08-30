# Deploy to Google Cloud Run (with Google Sheets logging)

## Prereqs (one-time in your GCP project)
1) Enable APIs:
   - Cloud Run, Cloud Build, Artifact Registry
2) Create/download your **service account JSON** that has access to Google Sheets API (Editor on your target Sheet).
3) Share your Google Sheet with the service account email as **Editor**.

## Build (Cloud Shell or local with gcloud)
```bash
# From repo root (where this file and Dockerfile live)
gcloud builds submit --tag gcr.io/PROJECT_ID/multicoin-bot
$env:SPREADSHEET_ID = "YOUR_SHEET_ID"
$env:GOOGLE_SERVICE_ACCOUNT_JSON = "{...your service account json...}"
python -u run_paper.py
$env:SPREADSHEET_ID = "YOUR_SHEET_ID"
$env:GOOGLE_SERVICE_ACCOUNT_JSON = "{...your service account json...}"
python -u run_paper.py
