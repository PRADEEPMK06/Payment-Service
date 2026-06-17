from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os

app = FastAPI(title="Payment Service")

# Prometheus Metrics Definition
PAYMENT_REQUESTS = Counter(
    'payment_requests_total', 
    'Total number of processed payments', 
    ['status']
)

@app.get("/")
def read_root():
    # Demonstrating the app can see the secret injected via AWS Secrets Manager
    db_pass = os.getenv("DB_PASSWORD", "Not Found")
    masked_pass = f"{db_pass[:3]}***" if len(db_pass) > 3 else "None"
    return {
        "service": "payment-service",
        "status": "active",
        "database_connection": f"Configured with pass: {masked_pass}"
    }

@app.post("/pay")
def process_payment():
    PAYMENT_REQUESTS.labels(status="success").inc()
    return {"transaction_id": "tx_98234710", "result": "approved"}

@app.get("/metrics")
def metrics():
    # Exposes endpoints for Prometheus scraping
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)