import asyncio
import logging
from pathlib import Path
from typing import List, Dict
import git
from git.exc import GitCommandError

from app.core.exceptions import GitCloneError, GitBlameError

logger = logging.getLogger(__name__)


class GitService:
    """Handles Git operations: clone, blame, and file filtering"""

    # File extensions to analyze (source code only)
    SUPPORTED_EXTENSIONS = {
        '.java', '.kt', '.py', '.js', '.ts', '.jsx', '.tsx',
        '.go', '.rs', '.cpp', '.c', '.h', '.hpp',
        '.rb', '.php', '.swift', '.scala', '.cs'
    }

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.repo = None

    async def clone_repository(self, repo_url: str, branch: str = "main"):
        """
        Clone repository with shallow depth to save memory

        Args:
            repo_url: Git repository URL
            branch: Branch name to clone

        Raises:
            GitCloneError: If clone operation fails
        """
        try:
            logger.info(f"Cloning {repo_url} (branch: {branch}) to {self.workspace_path}")

            # Create workspace directory
            self.workspace_path.mkdir(parents=True, exist_ok=True)

            # Run git clone in executor to avoid blocking
            loop = asyncio.get_event_loop()
            self.repo = await loop.run_in_executor(
                None,
                self._clone_sync,
                repo_url,
                branch
            )

            logger.info(f"Successfully cloned repository")

        except GitCommandError as e:
            raise GitCloneError(f"Failed to clone repository: {e}")
        except Exception as e:
            raise GitCloneError(f"Unexpected error during clone: {e}")

    def _clone_sync(self, repo_url: str, branch: str):
        """Synchronous clone operation"""
        return git.Repo.clone_from(
            repo_url,
            self.workspace_path,
            branch=branch,
            depth=1  # Shallow clone to save disk space and memory
        )

    async def filter_files_by_user(self, target_user: str) -> List[Dict[str, any]]:
        """
        Filter files that have at least 1 line contributed by target_user

        Args:
            target_user: GitHub username to filter by

        Returns:
            List of dicts containing file_path and user_lines

        Raises:
            GitBlameError: If blame operation fails
        """
        if not self.repo:
            raise GitBlameError("Repository not cloned yet")

        try:
            logger.info(f"Filtering files by user: {target_user}")

            filtered_files = []

            # Get all source code files
            for file_path in self.workspace_path.rglob("*"):
                if not file_path.is_file():
                    continue

                if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
                    continue

                # Get relative path
                rel_path = file_path.relative_to(self.workspace_path)

                # Skip if in .git directory
                if '.git' in rel_path.parts:
                    continue

                # Run blame analysis
                user_lines = await self._analyze_file_blame(str(rel_path), target_user)

                if user_lines > 0:
                    filtered_files.append({
                        "file_path": str(rel_path),
                        "absolute_path": str(file_path),
                        "user_lines": user_lines
                    })

            logger.info(f"Filtered {len(filtered_files)} files with contributions from {target_user}")
            return filtered_files

        except Exception as e:
            raise GitBlameError(f"Failed to filter files by user: {e}")

    async def _analyze_file_blame(self, rel_path: str, target_user: str) -> int:
        """
        Count lines contributed by target_user using git blame

        Args:
            rel_path: Relative file path from repository root
            target_user: GitHub username

        Returns:
            Number of lines contributed by target_user
        """
        try:
            loop = asyncio.get_event_loop()
            blame_output = await loop.run_in_executor(
                None,
                self._blame_sync,
                rel_path
            )

            # Count lines by target_user
            user_line_count = sum(
                1 for commit, lines in blame_output
                if commit.author.name == target_user or commit.author.email.startswith(target_user)
            )

            return user_line_count

        except GitCommandError:
            # File might be binary or have issues, skip it
            return 0
        except Exception as e:
            logger.warning(f"Error analyzing blame for {rel_path}: {e}")
            return 0

    def _blame_sync(self, rel_path: str):
        """Synchronous git blame operation"""
        return self.repo.blame('HEAD', rel_path)
