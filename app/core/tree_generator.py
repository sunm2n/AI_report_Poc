import os
from pathlib import Path
from typing import Set


class ProjectTreeGenerator:
    """Generates a text-based directory tree structure"""

    # Common directories and files to ignore
    IGNORE_DIRS = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv',
        'build', 'dist', '.idea', '.vscode', 'target'
    }

    IGNORE_FILES = {
        '.DS_Store', 'Thumbs.db', '.gitignore', '.env'
    }

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def generate(self, max_depth: int = 5) -> str:
        """
        Generate directory tree structure as string

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            String representation of the project tree
        """
        lines = []
        self._build_tree(self.workspace_path, "", lines, 0, max_depth)
        return "\n".join(lines)

    def _build_tree(
        self,
        directory: Path,
        prefix: str,
        lines: list,
        current_depth: int,
        max_depth: int
    ):
        """Recursively build tree structure"""
        if current_depth > max_depth:
            return

        try:
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            return

        # Filter out ignored items
        entries = [
            e for e in entries
            if e.name not in self.IGNORE_DIRS and e.name not in self.IGNORE_FILES
        ]

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                self._build_tree(
                    entry,
                    prefix + extension,
                    lines,
                    current_depth + 1,
                    max_depth
                )
