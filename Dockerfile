FROM python:3.12-slim

ARG BUILD_DATE
ARG GIT_SHA
LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${GIT_SHA}" \
      org.opencontainers.image.source="github.com/platform/app-repo"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Non-root user with its own group
RUN groupadd -r -g 1000 appuser && \
    useradd  -r -u 1000 -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 9898

# gunicorn for production — not the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:9898", "--workers", "2", "--timeout", "30", "src.main:app"]
