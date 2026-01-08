import logging
import re
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

logger = logging.getLogger(__name__)


class GroupingService:
    """Smart file grouping for providing context to AI"""

    # Common suffixes in class/file names
    COMMON_SUFFIXES = [
        'Controller', 'Service', 'ServiceImpl', 'Repository',
        'Dao', 'Dto', 'Entity', 'Model', 'Config',
        'Handler', 'Mapper', 'Util', 'Helper', 'Manager'
    ]

    def group_files(self, files: List[Dict[str, any]]) -> List[List[Dict[str, any]]]:
        """
        Group files using two-tier strategy:
        1. Name-based clustering (higher priority)
        2. Folder-based clustering (fallback)

        Args:
            files: List of file dicts with file_path, absolute_path, user_lines

        Returns:
            List of file groups (each group is a list of file dicts)
        """
        logger.info(f"Starting smart grouping for {len(files)} files")

        # Step 1: Name-based clustering
        name_groups = self._group_by_name(files)
        grouped_files = set()

        groups = []
        for group in name_groups.values():
            if len(group) > 0:
                groups.append(group)
                grouped_files.update(f["file_path"] for f in group)

        logger.info(f"Name-based grouping created {len(groups)} groups")

        # Step 2: Folder-based clustering for ungrouped files
        ungrouped_files = [
            f for f in files
            if f["file_path"] not in grouped_files
        ]

        if ungrouped_files:
            folder_groups = self._group_by_folder(ungrouped_files)
            groups.extend(folder_groups.values())
            logger.info(f"Folder-based grouping created {len(folder_groups)} additional groups")

        logger.info(f"Total groups created: {len(groups)}")
        return groups

    def _group_by_name(self, files: List[Dict[str, any]]) -> Dict[str, List[Dict[str, any]]]:
        """
        Group files by extracting core keyword from filename

        Example:
            UserController.java, UserService.java, UserServiceImpl.java
            -> All grouped under "User"
        """
        groups = defaultdict(list)

        for file_info in files:
            file_path = Path(file_info["file_path"])
            filename = file_path.stem  # Filename without extension

            # Extract core keyword by removing common suffixes
            core_keyword = self._extract_core_keyword(filename)

            if core_keyword:
                groups[core_keyword].append(file_info)

        # Filter out groups with only 1 file (no meaningful grouping)
        return {k: v for k, v in groups.items() if len(v) > 1}

    def _extract_core_keyword(self, filename: str) -> str:
        """
        Extract core keyword from filename by removing common suffixes

        Args:
            filename: File name without extension

        Returns:
            Core keyword (empty string if no suffix matched)
        """
        for suffix in self.COMMON_SUFFIXES:
            if filename.endswith(suffix):
                # Remove suffix and return core keyword
                core = filename[:-len(suffix)]
                if core:  # Ensure core is not empty
                    return core

        # No suffix matched, use full filename as keyword
        return filename

    def _group_by_folder(self, files: List[Dict[str, any]]) -> Dict[str, List[Dict[str, any]]]:
        """
        Group files that are in the same directory

        Args:
            files: List of ungrouped files

        Returns:
            Dict mapping folder path to list of files
        """
        groups = defaultdict(list)

        for file_info in files:
            file_path = Path(file_info["file_path"])
            folder = str(file_path.parent)

            groups[folder].append(file_info)

        return groups
