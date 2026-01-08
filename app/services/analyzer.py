import logging
from pathlib import Path

from app.config import settings
from app.core.semaphore import semaphore_manager
from app.core.exceptions import AnalysisError
from app.models.response import CallbackPayload, AnalysisResult
from app.utils.cleanup import cleanup_workspace
from app.services.git_service import GitService
from app.services.grouping_service import GroupingService
from app.services.ai_service import AIService
from app.services.callback_service import CallbackService
from app.core.tree_generator import ProjectTreeGenerator

logger = logging.getLogger(__name__)


async def analyze_repository(
    repo_url: str,
    branch: str,
    target_user: str,
    report_id: int,
    callback_url: str
):
    """
    Main analysis pipeline orchestrator

    Steps:
    1. Acquire global semaphore
    2. Clone repository
    3. Filter files by target_user
    4. Generate project tree
    5. Group files smartly
    6. AI Map analysis (parallel)
    7. AI Reduce analysis
    8. Send results to Spring
    9. Cleanup workspace
    """
    workspace_path = Path(settings.temp_workspace) / str(report_id)

    try:
        logger.info(f"[Report #{report_id}] Starting analysis pipeline")

        # Step 1: Acquire global semaphore
        await semaphore_manager.acquire_global()
        logger.info(f"[Report #{report_id}] Acquired global semaphore")

        try:
            # Step 2: Clone repository and filter files
            git_service = GitService(str(workspace_path))
            await git_service.clone_repository(repo_url, branch)
            filtered_files = await git_service.filter_files_by_user(target_user)

            if not filtered_files:
                raise AnalysisError(f"No files found for user '{target_user}'")

            logger.info(f"[Report #{report_id}] Found {len(filtered_files)} files by {target_user}")

            # Step 3: Generate project tree
            tree_generator = ProjectTreeGenerator(str(workspace_path))
            project_tree = tree_generator.generate()
            logger.info(f"[Report #{report_id}] Generated project tree")

            # Step 4: Group files smartly
            grouping_service = GroupingService()
            file_groups = grouping_service.group_files(filtered_files)
            logger.info(f"[Report #{report_id}] Grouped into {len(file_groups)} clusters")

            # Step 5: AI Map analysis
            ai_service = AIService()
            map_results = await ai_service.map_analysis(file_groups, str(workspace_path))
            logger.info(f"[Report #{report_id}] Completed Map analysis")

            # Step 6: AI Reduce analysis
            final_result = await ai_service.reduce_analysis(map_results, project_tree)
            logger.info(f"[Report #{report_id}] Completed Reduce analysis")

            # Step 7: Send results to Spring
            callback_service = CallbackService()
            payload = CallbackPayload(
                status="COMPLETED",
                result=AnalysisResult(**final_result)
            )
            await callback_service.send_result(callback_url, payload)
            logger.info(f"[Report #{report_id}] Sent results to Spring")

        finally:
            # Always release global semaphore
            semaphore_manager.release_global()
            logger.info(f"[Report #{report_id}] Released global semaphore")

    except Exception as e:
        logger.error(f"[Report #{report_id}] Analysis failed: {e}", exc_info=True)

        # Send failure callback
        try:
            callback_service = CallbackService()
            payload = CallbackPayload(
                status="FAILED",
                error_message=str(e)
            )
            await callback_service.send_result(callback_url, payload)
        except Exception as callback_error:
            logger.error(f"[Report #{report_id}] Failed to send error callback: {callback_error}")

    finally:
        # Step 8: Cleanup workspace
        await cleanup_workspace(str(workspace_path))
        logger.info(f"[Report #{report_id}] Analysis pipeline finished")
