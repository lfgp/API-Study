import json
from pathlib import Path

from storage.jason_handler import JSONHandler


def test_load_students_creates_default_file(tmp_path):
    handler = JSONHandler(base_dir=str(tmp_path))

    students = handler.load_students()

    assert len(students) >= 3
    assert (tmp_path / "students" / "students.json").exists()


def test_save_generation_and_history_filter(tmp_path):
    handler = JSONHandler(base_dir=str(tmp_path))

    handler.save_generation(
        student_id="1",
        topic="fracoes",
        content_type="conceptual",
        prompt_version="v1",
        model="gpt-4o-mini",
        prompt_messages=[{"role": "user", "content": "x"}],
        response_text="conteudo 1",
        used_cache=False,
    )
    handler.save_generation(
        student_id="2",
        topic="equacoes",
        content_type="examples",
        prompt_version="v2",
        model="gpt-4o-mini",
        prompt_messages=[{"role": "user", "content": "y"}],
        response_text="conteudo 2",
        used_cache=True,
    )

    all_items = handler.get_generation_history(limit=10)
    only_student_1 = handler.get_generation_history(student_id="1", limit=10)

    assert len(all_items) == 2
    assert len(only_student_1) == 1
    assert only_student_1[0]["student_id"] == "1"


def test_get_student_by_id(tmp_path):
    handler = JSONHandler(base_dir=str(tmp_path))
    handler.save_students([
        {
            "id": "abc",
            "name": "Teste",
            "age": 20,
            "level": "iniciante",
            "style": "visual",
            "interests": [],
        }
    ])

    student = handler.get_student_by_id("abc")
    assert student is not None
    assert student["name"] == "Teste"
