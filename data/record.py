from __future__ import annotations

from typing import Any, Dict, List, Optional

from storage.jason_handler import JSONHandler


def list_generation_history(data_dir: str = "./data", student_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Returns generation history entries from JSON storage."""
    handler = JSONHandler(data_dir)
    return handler.get_generation_history(student_id=student_id, limit=limit)
