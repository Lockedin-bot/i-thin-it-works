FROM python:3.11-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 TZ=Etc/UTC
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
COPY . .
CMD bash -lc "cp -n .env.fast_test .env || true; python -u app_server.py"
