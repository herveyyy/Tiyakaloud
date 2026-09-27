import os
import sys
from pathlib import Path
from fastapi import FastAPI
import uvicorn

# Ensure the package root is in sys.path for direct script execution
PACKAGE_ROOT = Path(__file__).resolve().parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from controllers import health_router, predict_router, systemone_router

app = FastAPI(
    title="Laya Decision & Routing Server",
    description="Fast, non-autoregressive System 1 decision engine and classification service powered by Laya",
    version="1.0.0",
)

# Register routers from controllers
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(systemone_router)


@app.get("/")
def root():
    return {
        "service": "Laya Decision Server",
        "status": "online",
        "docs_url": "/docs",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "predict_ticket": "POST /predict/ticket",
            "systemone": "POST /v1/systemone",
        },
    }


def run():
    host = os.environ.get("LAYA_HOST", "0.0.0.0")
    port = int(os.environ.get("LAYA_PORT", "8000"))
    print(f"\n========================================================")
    print(f"  Starting Laya Server on http://{host}:{port}")
    print(f"  Interactive Swagger UI: http://localhost:{port}/docs")
    print(f"========================================================\n")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()