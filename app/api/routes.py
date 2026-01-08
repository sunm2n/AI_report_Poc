from fastapi import APIRouter, BackgroundTasks, HTTPException, status
import logging

from app.models.request import AnalyzeRequest
from app.models.response import AnalyzeResponse
from app.core.semaphore import semaphore_manager
from app.services.analyzer import analyze_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis(
    request: AnalyzeRequest,
    background_tasks: BackgroundTasks
):
    """
    Queue a repository analysis task

    Returns 202 Accepted immediately and processes analysis in background

    - **repo_url**: GitHub repository URL
    - **branch**: Branch to analyze (default: main)
    - **target_user**: GitHub username to analyze contributions for
    - **report_id**: Spring DB primary key for this report
    - **callback_url**: Spring endpoint to PATCH results to
    """
    logger.info(f"Received analysis request for Report #{request.report_id}")
    logger.info(f"Repository: {request.repo_url}, User: {request.target_user}")

    # Check if global semaphore is available
    if semaphore_manager.global_semaphore.locked():
        # Calculate current queue size
        current_queue = semaphore_manager.global_semaphore._value
        if current_queue <= 0:
            logger.warning(f"Global queue full, rejecting Report #{request.report_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Analysis queue is full. Please try again later."
            )

    # Add analysis task to background
    background_tasks.add_task(
        analyze_repository,
        repo_url=request.repo_url,
        branch=request.branch,
        target_user=request.target_user,
        report_id=request.report_id,
        callback_url=request.callback_url
    )

    return AnalyzeResponse(
        status="ACCEPTED",
        message=f"Analysis queued for Report #{request.report_id}"
    )
