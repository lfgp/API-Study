from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify, request
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

try:
    from flask_cors import CORS
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal test envs
    def CORS(_app):
        return None

from core.generator import ContentGenerator
from core.prompt_engine import CONTENT_TYPES
from core.student import Student
from storage.jason_handler import JSONHandler


load_dotenv()

app = Flask(__name__)
CORS(app)

config: dict[str, Any] = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "OPENAI_ORG_ID": os.getenv("OPENAI_ORG_ID", ""),
    "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", ""),
    "STANDARD_MODEL": os.getenv("STANDARD_MODEL", "gpt-4o-mini"),
    "STANDARD_TEMPERATURE": os.getenv("STANDARD_TEMPERATURE", "0.7"),
    "STANDARD_MAX_TOKENS": os.getenv("STANDARD_MAX_TOKENS", "1200"),
    "CACHE_TYPE": os.getenv("CACHE_TYPE", "disk"),
    "CACHE_DIR": os.getenv("CACHE_DIR", "./cache"),
    "CACHE_TTL": os.getenv("CACHE_TTL", "3600"),
    "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    "DATA_DIR": os.getenv("DATA_DIR", "./data"),
}

generator = ContentGenerator(config)
storage = JSONHandler(config["DATA_DIR"])


def _get_student_or_error(student_id: str):
    data = storage.get_student_by_id(student_id)
    if not data:
        return None, (jsonify({"error": "Student not found"}), 404)
    return Student(**data), None


@app.route("/", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "API-Study",
            "endpoints": [
                "GET /api/students",
                "POST /api/students",
                "POST /api/generate",
                "POST /api/generate-all",
                "POST /api/compare",
                "GET /api/history",
            ],
        }
    )


@app.route("/api/students", methods=["GET"])
def list_students():
    return jsonify(storage.load_students())


@app.route("/api/students", methods=["POST"])
def create_student():
    payload = request.json or {}
    try:
        student = Student(**payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    students = storage.load_students()
    students.append(student.model_dump(mode="json"))
    storage.save_students(students)
    return jsonify(student.model_dump(mode="json")), 201


@app.route("/api/generate", methods=["POST"])
def generate_single():
    payload = request.json or {}
    required = {"student_id", "topic", "type"}
    if not required.issubset(payload.keys()):
        return jsonify({"error": f"Missing fields: {sorted(required)}"}), 400

    if payload["type"] not in CONTENT_TYPES:
        return jsonify({"error": f"Invalid type. Allowed: {list(CONTENT_TYPES)}"}), 400

    student, error = _get_student_or_error(payload["student_id"])
    if error:
        return error

    result = asyncio.run(
        generator.generate_content(
            student=student,
            topic=payload["topic"],
            content_type=payload["type"],
            prompt_version=payload.get("prompt_version", "v1"),
            use_cache=bool(payload.get("use_cache", True)),
        )
    )
    return jsonify(result)


@app.route("/api/generate-all", methods=["POST"])
def generate_all():
    payload = request.json or {}
    required = {"student_id", "topic"}
    if not required.issubset(payload.keys()):
        return jsonify({"error": f"Missing fields: {sorted(required)}"}), 400

    student, error = _get_student_or_error(payload["student_id"])
    if error:
        return error

    result = asyncio.run(
        generator.generate_all_types(
            student=student,
            topic=payload["topic"],
            prompt_version=payload.get("prompt_version", "v1"),
            use_cache=bool(payload.get("use_cache", True)),
        )
    )
    return jsonify(result)


@app.route("/api/compare", methods=["POST"])
def compare_versions():
    payload = request.json or {}
    required = {"student_id", "topic", "type"}
    if not required.issubset(payload.keys()):
        return jsonify({"error": f"Missing fields: {sorted(required)}"}), 400

    if payload["type"] not in CONTENT_TYPES:
        return jsonify({"error": f"Invalid type. Allowed: {list(CONTENT_TYPES)}"}), 400

    student, error = _get_student_or_error(payload["student_id"])
    if error:
        return error

    versions = tuple(payload.get("versions", ["v1", "v2"]))
    result = asyncio.run(
        generator.compare_prompt_versions(
            student=student,
            topic=payload["topic"],
            content_type=payload["type"],
            versions=versions,
            use_cache=bool(payload.get("use_cache", False)),
        )
    )
    return jsonify(result)


@app.route("/api/history", methods=["GET"])
def history():
    student_id = request.args.get("student_id")
    limit = int(request.args.get("limit", 50))
    return jsonify(storage.get_generation_history(student_id=student_id, limit=limit))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
