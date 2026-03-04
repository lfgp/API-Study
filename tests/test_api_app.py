import pytest
import importlib

from storage.jason_handler import JSONHandler

api_app = importlib.import_module("api.app")


@pytest.fixture
def client(tmp_path, monkeypatch):
    storage = JSONHandler(base_dir=str(tmp_path))
    monkeypatch.setattr(api_app, "storage", storage)

    class DummyGenerator:
        async def generate_content(self, **kwargs):
            return {
                "student_id": kwargs["student"].id,
                "topic": kwargs["topic"],
                "content_type": kwargs["content_type"],
                "prompt_version": kwargs["prompt_version"],
                "model": "mock-model",
                "used_cache": kwargs["use_cache"],
                "response": "mocked response",
            }

        async def generate_all_types(self, **kwargs):
            return {
                "student_id": kwargs["student"].id,
                "topic": kwargs["topic"],
                "prompt_version": kwargs["prompt_version"],
                "model": "mock-model",
                "types": ["conceptual", "examples", "reflection", "visual"],
                "results": {},
                "bundle_file": "tmp/bundle.json",
            }

        async def compare_prompt_versions(self, **kwargs):
            return {
                "student_id": kwargs["student"].id,
                "topic": kwargs["topic"],
                "content_type": kwargs["content_type"],
                "versions": {
                    "v1": {"response": "v1"},
                    "v2": {"response": "v2"},
                },
                "comparison_file": "tmp/comparison.json",
            }

    monkeypatch.setattr(api_app, "generator", DummyGenerator())

    api_app.app.config["TESTING"] = True
    with api_app.app.test_client() as test_client:
        yield test_client, storage


def test_list_students(client):
    test_client, _ = client
    response = test_client.get("/api/students")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_student(client):
    test_client, storage = client
    payload = {
        "id": "999",
        "name": "Novo Aluno",
        "age": 18,
        "level": "intermediario",
        "style": "visual",
        "interests": ["matematica"],
    }
    response = test_client.post("/api/students", json=payload)

    assert response.status_code == 201
    created = response.get_json()
    assert created["id"] == "999"
    assert storage.get_student_by_id("999") is not None


def test_generate_validates_missing_fields(client):
    test_client, _ = client
    response = test_client.post("/api/generate", json={"student_id": "1"})
    assert response.status_code == 400


def test_generate_rejects_invalid_type(client):
    test_client, _ = client
    response = test_client.post(
        "/api/generate",
        json={"student_id": "1", "topic": "fracoes", "type": "invalid"},
    )
    assert response.status_code == 400


def test_generate_success(client):
    test_client, _ = client
    response = test_client.post(
        "/api/generate",
        json={"student_id": "1", "topic": "fracoes", "type": "conceptual"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == "mocked response"


def test_compare_success(client):
    test_client, _ = client
    response = test_client.post(
        "/api/compare",
        json={"student_id": "1", "topic": "fracoes", "type": "conceptual"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "versions" in data


def test_history_endpoint(client):
    test_client, storage = client
    storage.save_generation(
        student_id="1",
        topic="fracoes",
        content_type="conceptual",
        prompt_version="v1",
        model="mock-model",
        prompt_messages=[{"role": "user", "content": "p"}],
        response_text="r",
        used_cache=False,
    )

    response = test_client.get("/api/history?student_id=1&limit=10")
    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert payload[0]["student_id"] == "1"
