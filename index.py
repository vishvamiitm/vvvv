import math

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="eShopCo Latency Metrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Telemetry from the supplied sample bundle.
TELEMETRY = [{'region': 'apac', 'service': 'checkout', 'latency_ms': 219.23, 'uptime_pct': 97.71, 'timestamp': 20250301}, {'region': 'apac', 'service': 'catalog', 'latency_ms': 223.91, 'uptime_pct': 98.485, 'timestamp': 20250302}, {'region': 'apac', 'service': 'checkout', 'latency_ms': 211.74, 'uptime_pct': 98.26, 'timestamp': 20250303}, {'region': 'apac', 'service': 'support', 'latency_ms': 226.44, 'uptime_pct': 98.555, 'timestamp': 20250304}, {'region': 'apac', 'service': 'recommendations', 'latency_ms': 194.62, 'uptime_pct': 98.358, 'timestamp': 20250305}, {'region': 'apac', 'service': 'payments', 'latency_ms': 217.28, 'uptime_pct': 98.873, 'timestamp': 20250306}, {'region': 'apac', 'service': 'catalog', 'latency_ms': 168.21, 'uptime_pct': 98.437, 'timestamp': 20250307}, {'region': 'apac', 'service': 'support', 'latency_ms': 191.6, 'uptime_pct': 98.949, 'timestamp': 20250308}, {'region': 'apac', 'service': 'support', 'latency_ms': 142.53, 'uptime_pct': 98.575, 'timestamp': 20250309}, {'region': 'apac', 'service': 'checkout', 'latency_ms': 107.02, 'uptime_pct': 99.157, 'timestamp': 20250310}, {'region': 'apac', 'service': 'checkout', 'latency_ms': 146.27, 'uptime_pct': 98.418, 'timestamp': 20250311}, {'region': 'apac', 'service': 'analytics', 'latency_ms': 186.28, 'uptime_pct': 97.412, 'timestamp': 20250312}, {'region': 'emea', 'service': 'catalog', 'latency_ms': 192.72, 'uptime_pct': 99.418, 'timestamp': 20250301}, {'region': 'emea', 'service': 'catalog', 'latency_ms': 115.55, 'uptime_pct': 97.296, 'timestamp': 20250302}, {'region': 'emea', 'service': 'recommendations', 'latency_ms': 172.01, 'uptime_pct': 98.366, 'timestamp': 20250303}, {'region': 'emea', 'service': 'catalog', 'latency_ms': 121.05, 'uptime_pct': 98.315, 'timestamp': 20250304}, {'region': 'emea', 'service': 'support', 'latency_ms': 140.67, 'uptime_pct': 97.82, 'timestamp': 20250305}, {'region': 'emea', 'service': 'support', 'latency_ms': 186.39, 'uptime_pct': 97.495, 'timestamp': 20250306}, {'region': 'emea', 'service': 'catalog', 'latency_ms': 163, 'uptime_pct': 97.609, 'timestamp': 20250307}, {'region': 'emea', 'service': 'analytics', 'latency_ms': 198.19, 'uptime_pct': 98.883, 'timestamp': 20250308}, {'region': 'emea', 'service': 'support', 'latency_ms': 203.2, 'uptime_pct': 99.146, 'timestamp': 20250309}, {'region': 'emea', 'service': 'checkout', 'latency_ms': 134.95, 'uptime_pct': 97.121, 'timestamp': 20250310}, {'region': 'emea', 'service': 'checkout', 'latency_ms': 201.96, 'uptime_pct': 97.898, 'timestamp': 20250311}, {'region': 'emea', 'service': 'support', 'latency_ms': 205.72, 'uptime_pct': 99.276, 'timestamp': 20250312}, {'region': 'amer', 'service': 'catalog', 'latency_ms': 146.83, 'uptime_pct': 97.707, 'timestamp': 20250301}, {'region': 'amer', 'service': 'payments', 'latency_ms': 174.23, 'uptime_pct': 97.245, 'timestamp': 20250302}, {'region': 'amer', 'service': 'payments', 'latency_ms': 144.31, 'uptime_pct': 98.265, 'timestamp': 20250303}, {'region': 'amer', 'service': 'checkout', 'latency_ms': 156.39, 'uptime_pct': 97.952, 'timestamp': 20250304}, {'region': 'amer', 'service': 'catalog', 'latency_ms': 122.01, 'uptime_pct': 99.422, 'timestamp': 20250305}, {'region': 'amer', 'service': 'catalog', 'latency_ms': 107.68, 'uptime_pct': 98.266, 'timestamp': 20250306}, {'region': 'amer', 'service': 'payments', 'latency_ms': 148.25, 'uptime_pct': 97.182, 'timestamp': 20250307}, {'region': 'amer', 'service': 'recommendations', 'latency_ms': 128.57, 'uptime_pct': 97.64, 'timestamp': 20250308}, {'region': 'amer', 'service': 'checkout', 'latency_ms': 165.13, 'uptime_pct': 97.98, 'timestamp': 20250309}, {'region': 'amer', 'service': 'support', 'latency_ms': 225.26, 'uptime_pct': 97.982, 'timestamp': 20250310}, {'region': 'amer', 'service': 'payments', 'latency_ms': 223.67, 'uptime_pct': 98.324, 'timestamp': 20250311}, {'region': 'amer', 'service': 'analytics', 'latency_ms': 215.32, 'uptime_pct': 98.728, 'timestamp': 20250312}]


class MetricsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float = Field(default=180, ge=0)


def percentile_95(values: list[float]) -> float:
    """Linear-interpolated 95th percentile."""
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = 0.95 * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


@app.get("/")
def health():
    return {"status": "ok", "endpoint": "/api/index"}


@app.post("/api/index")
def calculate_metrics(request: MetricsRequest):
    response = {}
    for region in request.regions:
        rows = [r for r in TELEMETRY if r.get("region") == region]
        latencies = [float(r["latency_ms"]) for r in rows]
        uptimes = [float(r["uptime_pct"]) for r in rows]

        if not rows:
            response[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0,
            }
            continue

        response[region] = {
            "avg_latency": sum(latencies) / len(latencies),
            "p95_latency": percentile_95(latencies),
            "avg_uptime": sum(uptimes) / len(uptimes),
            "breaches": sum(value > request.threshold_ms for value in latencies),
        }
    return response
