from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class KnowledgeLevel(str, Enum):
    BEGINNER = "iniciante"
    INTERMEDIATE = "intermediario"
    ADVANCED = "avancado"


class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditivo"
    READING_WRITING = "leitura-escrita"
    KINESTHETIC = "cinestesico"


class Student(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    age: int = Field(ge=0, le=120)
    level: KnowledgeLevel
    style: LearningStyle
    interests: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Name cannot be empty")
        return cleaned.title()

    def build_persona_prompt(self) -> str:
        return (
            "Voce e um professor experiente em Pedagogia, especialista em personalizar "
            "explicacoes para diferentes perfis de estudantes."
        )

    def build_student_context(self, topic: str) -> str:
        return (
            f"Estudante: {self.name} | Idade: {self.age} | Nivel: {self.level.value} | "
            f"Estilo: {self.style.value} | Interesses: {', '.join(self.interests) or 'nao informado'} | "
            f"Topico: {topic}"
        )


# Portuguese aliases kept only for compatibility with existing code.
Estudante = Student
NivelConhecimento = KnowledgeLevel
EstiloAprendizado = LearningStyle
Aluno = Student
