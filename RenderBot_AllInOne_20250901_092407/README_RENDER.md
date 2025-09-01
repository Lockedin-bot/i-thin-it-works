# Render-ready bot

Endpoints:
- \/health\  ok
- \/status\  JSON with recent heartbeats & trades

## Local test
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.fast_test .env
python -u app_server.py
# open http://localhost:10000/status

## Deploy on Render
- Connect this repo as a **Web Service (Environment: Docker)**
- Leave Start Command blank (Dockerfile CMD runs app_server.py)
- Health check path: \/health\
- Persistent Disk: mount \/app/logs\ (1 GB)
