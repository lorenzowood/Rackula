FROM python:3.12-alpine AS base

FROM base AS deps
WORKDIR /app
COPY requirements.txt .
# Only install runtime deps (no pytest/httpx)
RUN pip install --no-cache-dir fastapi>=0.115 "uvicorn[standard]>=0.32" pyyaml>=6.0

FROM base AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 rackula && \
    adduser --system --uid 1001 --ingroup rackula rackula

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY app.py storage.py ./

RUN mkdir -p /data && chown rackula:rackula /data

LABEL org.opencontainers.image.source="https://github.com/RackulaLives/Rackula"
LABEL org.opencontainers.image.description="Rackula API Sidecar (Python)"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="Rackula API"

USER rackula

ENV DATA_DIR=/data \
    RACKULA_API_PORT=3001 \
    CORS_ORIGIN=http://localhost:8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 3001

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3001/health || exit 1

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${RACKULA_API_PORT:-3001} --workers 1"]
