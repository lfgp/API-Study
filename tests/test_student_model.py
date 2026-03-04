import pytest
from pydantic import ValidationError

from core.student import Student


def test_student_name_is_normalized():
    student = Student(
        id="st-1",
        name="  maria oliveira  ",
        age=14,
        level="intermediario",
        style="visual",
    )
    assert student.name == "Maria Oliveira"


def test_student_name_cannot_be_empty():
    with pytest.raises(ValidationError):
        Student(
            id="st-1",
            name="   ",
            age=14,
            level="intermediario",
            style="visual",
        )


def test_build_student_context_contains_expected_data():
    student = Student(
        id="st-2",
        name="Ana",
        age=10,
        level="iniciante",
        style="auditivo",
        interests=["musica"],
    )
    context = student.build_student_context("fracoes")

    assert "Ana" in context
    assert "fracoes" in context
    assert "iniciante" in context
    assert "auditivo" in context
