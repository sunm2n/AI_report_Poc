import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def cleanup_workspace(workspace_path: str):
    """
    Remove temporary workspace directory

    Args:
        workspace_path: Path to the temporary workspace
    """
    try:
        path = Path(workspace_path)
        if path.exists() and path.is_dir():
            shutil.rmtree(workspace_path)
            logger.info(f"Cleaned up workspace: {workspace_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup workspace {workspace_path}: {e}")
