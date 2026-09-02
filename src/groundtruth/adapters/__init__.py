"""GroundTruth Storage Adapters."""

from groundtruth.adapters.base import DataRepository
from groundtruth.adapters.git_file import GitFileDataAdapter
from groundtruth.adapters.sqlite import SQLiteDataAdapter

__all__ = [
    "DataRepository",
    "GitFileDataAdapter",
    "SQLiteDataAdapter",
]

