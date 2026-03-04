import pytest

from core.prompt_engine import CONTENT_TYPES, PromptEngine
from core.student import Student


@pytest.fixture
def sample_student() -> Student:
    return Student(
        id="s-1",
        name="Carlos",
        age=16,
        level="intermediario",
        style="leitura-escrita",
        interests=["tecnologia"],
    )


def test_prompt_engine_rejects_invalid_version(sample_student):
    with pytest.raises(ValueError):
        PromptEngine(sample_student, "logica", prompt_version="v9")


def test_prompt_engine_rejects_invalid_content_type(sample_student):
    engine = PromptEngine(sample_student, "logica", prompt_version="v1")
    with pytest.raises(ValueError):
        engine.build_messages("invalid")


def test_prompt_engine_builds_messages_for_all_content_types(sample_student):
    engine = PromptEngine(sample_student, "logica", prompt_version="v1")

    for content_type in CONTENT_TYPES:
        messages = engine.build_messages(content_type)
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert "logica" in messages[1]["content"]


def test_prompt_engine_v2_changes_instruction_style(sample_student):
    engine_v2 = PromptEngine(sample_student, "logica", prompt_version="v2")
    msg = engine_v2.build_messages("conceptual")[1]["content"]
    assert "mini-checklist" in msg
