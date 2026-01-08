"""
Mock Spring Server for testing FastAPI callbacks

Run this server to simulate Spring backend during POC testing:
    python tests/mock_spring.py

It will listen on port 9000 and accept PATCH requests at /api/reports/{report_id}
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Mock Spring Server")

# In-memory storage for reports
reports = {}


@app.patch("/api/reports/{report_id}")
async def update_report(report_id: int, request: Request):
    """
    Mock endpoint that receives analysis results from FastAPI

    Matches Spring's PATCH /api/reports/{report_id} endpoint
    """
    payload = await request.json()

    logger.info("=" * 70)
    logger.info(f"Received callback for Report #{report_id}")
    logger.info(f"Status: {payload.get('status')}")

    if payload.get('status') == 'COMPLETED':
        result = payload.get('result', {})
        logger.info("\n" + "=" * 70)
        logger.info("ANALYSIS RESULT")
        logger.info("=" * 70)
        logger.info(f"\nSummary:\n{result.get('summary', 'N/A')}")
        logger.info(f"\nTech Stack:\n{', '.join(result.get('tech_stack', []))}")
        logger.info(f"\nKey Contributions:")
        for i, contrib in enumerate(result.get('key_contributions', []), 1):
            logger.info(f"  {i}. {contrib}")
        logger.info(f"\nCode Quality:\n{result.get('code_quality', 'N/A')}")
        logger.info(f"\nProject Tree:\n{result.get('project_tree', 'N/A')[:500]}...")
        logger.info("=" * 70)

    elif payload.get('status') == 'FAILED':
        error_message = payload.get('error_message', 'Unknown error')
        logger.error(f"\nAnalysis FAILED: {error_message}")
        logger.error("=" * 70)

    # Store result
    reports[report_id] = {
        "payload": payload,
        "received_at": datetime.now().isoformat()
    }

    return JSONResponse(
        status_code=200,
        content={"message": f"Report #{report_id} updated successfully"}
    )


@app.get("/api/reports/{report_id}")
async def get_report(report_id: int):
    """Retrieve stored report data"""
    if report_id in reports:
        return reports[report_id]
    else:
        return JSONResponse(
            status_code=404,
            content={"error": f"Report #{report_id} not found"}
        )


@app.get("/")
async def root():
    return {
        "service": "Mock Spring Server",
        "status": "running",
        "reports_received": len(reports)
    }


if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("Starting Mock Spring Server on http://localhost:9000")
    logger.info("Waiting for callbacks from FastAPI...")
    logger.info("=" * 70)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000,
        log_level="info"
    )
