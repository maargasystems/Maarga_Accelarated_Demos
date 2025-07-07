# ─────────────────────────── Dockerfile ───────────────────────────
FROM python:3.10-slim

# 1. (Optional) install git if any pip packages come from GitHub
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

# 2. Workdir inside the container
WORKDIR /app

# 3. Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the source tree (including maarga_logo.png)
COPY . .

# 5. Default port (can be overridden via docker‑compose)
ENV PORT=8500
EXPOSE ${PORT}

# 6. Run Streamlit on the chosen port
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
