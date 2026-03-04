from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class JSONHandler:
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = Path(base_dir)
        self.students_dir = self.base_dir / "students"
        self.generations_dir = self.base_dir / "generations"
        self.comparisons_dir = self.base_dir / "comparisons"
        self.students_file = self.students_dir / "students.json"
        self._create_dirs()

    def _create_dirs(self) -> None:
        self.students_dir.mkdir(parents=True, exist_ok=True)
        self.generations_dir.mkdir(parents=True, exist_ok=True)
        self.comparisons_dir.mkdir(parents=True, exist_ok=True)

    def load_students(self) -> List[Dict[str, Any]]:
        if not self.students_file.exists():
            students = self._create_default_students()
            self.save_students(students)
            return students

        with open(self.students_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("students", [])

    def save_students(self, students: List[Dict[str, Any]]) -> str:
        payload = {
            "updated_at": datetime.utcnow().isoformat(),
            "students_total": len(students),
            "students": students,
        }
        with open(self.students_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)
        return str(self.students_file)

    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        return next((student for student in self.load_students() if student.get("id") == student_id), None)

    def save_generation(
        self,
        student_id: str,
        topic: str,
        content_type: str,
        prompt_version: str,
        model: str,
        prompt_messages: List[Dict[str, str]],
        response_text: str,
        used_cache: bool,
    ) -> str:
        timestamp = datetime.utcnow().isoformat()
        digest = hashlib.md5(f"{student_id}|{topic}|{content_type}|{prompt_version}|{timestamp}".encode()).hexdigest()[:10]
        filename = self.generations_dir / f"{student_id}_{content_type}_{prompt_version}_{digest}.json"

        payload = {
            "timestamp": timestamp,
            "student_id": student_id,
            "topic": topic,
            "content_type": content_type,
            "prompt_version": prompt_version,
            "model": model,
            "used_cache": used_cache,
            "prompt": prompt_messages,
            "response": response_text,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)

        return str(filename)

    def save_bundle(
        self,
        student_id: str,
        topic: str,
        prompt_version: str,
        model: str,
        results: Dict[str, Dict[str, Any]],
    ) -> str:
        timestamp = datetime.utcnow().isoformat()
        digest = hashlib.md5(f"{student_id}|{topic}|{prompt_version}|bundle|{timestamp}".encode()).hexdigest()[:10]
        filename = self.generations_dir / f"bundle_{student_id}_{prompt_version}_{digest}.json"

        payload = {
            "timestamp": timestamp,
            "student_id": student_id,
            "topic": topic,
            "prompt_version": prompt_version,
            "model": model,
            "results": results,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)

        return str(filename)

    def save_comparison(
        self,
        student_id: str,
        topic: str,
        content_type: str,
        comparison: Dict[str, Any],
    ) -> str:
        timestamp = datetime.utcnow().isoformat()
        digest = hashlib.md5(f"{student_id}|{topic}|{content_type}|comparison|{timestamp}".encode()).hexdigest()[:10]
        filename = self.comparisons_dir / f"comparison_{student_id}_{content_type}_{digest}.json"

        payload = {
            "timestamp": timestamp,
            "student_id": student_id,
            "topic": topic,
            "content_type": content_type,
            "comparison": comparison,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)

        return str(filename)

    def get_generation_history(self, student_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for file_path in self.generations_dir.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if student_id and data.get("student_id") != student_id:
                    continue
                items.append(data)

        items.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
        return items[:limit]

    def _create_default_students(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "1",
                "name": "Ana Silva",
                "age": 8,
                "level": "iniciante",
                "style": "visual",
                "interests": ["animais", "desenho"],
            },
            {
                "id": "2",
                "name": "Joao Santos",
                "age": 15,
                "level": "intermediario",
                "style": "cinestesico",
                "interests": ["esportes", "videogame"],
            },
            {
                "id": "3",
                "name": "Maria Oliveira",
                "age": 25,
                "level": "avancado",
                "style": "leitura-escrita",
                "interests": ["programacao", "ciencia"],
            },
            {
                "id": "4",
                "name": "Pedro Costa",
                "age": 35,
                "level": "intermediario",
                "style": "auditivo",
                "interests": ["musica", "historia"],
            },
            {
                "id": "5",
                "name": "Lucia Pereira",
                "age": 45,
                "level": "iniciante",
                "style": "visual",
                "interests": ["jardinagem", "culinaria"],
            },
        ]


# Backward-compatible alias for existing imports.
JasonHandler = JSONHandler
