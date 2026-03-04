from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.student import Student
from storage.jason_handler import JSONHandler


def list_students(data_dir: str = "./data") -> List[Student]:
    """Loads all students from JSON storage."""
    handler = JSONHandler(data_dir)
    return [Student(**item) for item in handler.load_students()]


def get_student(student_id: str, data_dir: str = "./data") -> Optional[Student]:
    """Loads a student by id from JSON storage."""
    handler = JSONHandler(data_dir)
    payload: Optional[Dict[str, Any]] = handler.get_student_by_id(student_id)
    return Student(**payload) if payload else None
