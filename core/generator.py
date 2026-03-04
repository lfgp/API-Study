from __future__ import annotations

from typing import Any, Dict, Iterable

from openai import AsyncOpenAI

from .prompt_engine import CONTENT_TYPES, PromptEngine
from .student import Student
from storage.cache_manager import CacheManager
from storage.jason_handler import JSONHandler


class ContentGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("STANDARD_MODEL", "gpt-4o-mini")
        self.temperature = float(config.get("STANDARD_TEMPERATURE", 0.7))
        self.max_tokens = int(config.get("STANDARD_MAX_TOKENS", 1200))
        self.client = AsyncOpenAI(
            api_key=config.get("OPENAI_API_KEY"),
            organization=config.get("OPENAI_ORG_ID") or None,
            base_url=config.get("OPENAI_BASE_URL") or None,
        )
        self.cache = CacheManager(config)
        self.storage = JSONHandler(config.get("DATA_DIR", "./data"))

    async def generate_content(
        self,
        student: Student,
        topic: str,
        content_type: str,
        prompt_version: str = "v1",
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        if content_type not in CONTENT_TYPES:
            raise ValueError(f"Invalid content_type '{content_type}'. Use one of: {CONTENT_TYPES}")

        engine = PromptEngine(student=student, topic=topic, prompt_version=prompt_version)
        messages = engine.build_messages(content_type)
        cache_key = CacheManager.make_key(student.id, topic, content_type, prompt_version, self.model)

        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                result = {
                    "student_id": student.id,
                    "topic": topic,
                    "content_type": content_type,
                    "prompt_version": prompt_version,
                    "model": self.model,
                    "used_cache": True,
                    "response": cached,
                }
                self.storage.save_generation(
                    student_id=student.id,
                    topic=topic,
                    content_type=content_type,
                    prompt_version=prompt_version,
                    model=self.model,
                    prompt_messages=messages,
                    response_text=cached,
                    used_cache=True,
                )
                return result

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        response_text = completion.choices[0].message.content.strip()

        self.cache.set(cache_key, response_text)
        self.storage.save_generation(
            student_id=student.id,
            topic=topic,
            content_type=content_type,
            prompt_version=prompt_version,
            model=self.model,
            prompt_messages=messages,
            response_text=response_text,
            used_cache=False,
        )

        return {
            "student_id": student.id,
            "topic": topic,
            "content_type": content_type,
            "prompt_version": prompt_version,
            "model": self.model,
            "used_cache": False,
            "response": response_text,
        }

    async def generate_all_types(
        self,
        student: Student,
        topic: str,
        prompt_version: str = "v1",
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        results: Dict[str, Dict[str, Any]] = {}
        for content_type in CONTENT_TYPES:
            results[content_type] = await self.generate_content(
                student=student,
                topic=topic,
                content_type=content_type,
                prompt_version=prompt_version,
                use_cache=use_cache,
            )

        bundle_path = self.storage.save_bundle(
            student_id=student.id,
            topic=topic,
            prompt_version=prompt_version,
            model=self.model,
            results=results,
        )

        return {
            "student_id": student.id,
            "topic": topic,
            "prompt_version": prompt_version,
            "model": self.model,
            "types": list(CONTENT_TYPES),
            "results": results,
            "bundle_file": bundle_path,
        }

    async def compare_prompt_versions(
        self,
        student: Student,
        topic: str,
        content_type: str,
        versions: Iterable[str] = ("v1", "v2"),
        use_cache: bool = False,
    ) -> Dict[str, Any]:
        comparison: Dict[str, Any] = {
            "student_id": student.id,
            "topic": topic,
            "content_type": content_type,
            "model": self.model,
            "versions": {},
        }

        for version in versions:
            comparison["versions"][version] = await self.generate_content(
                student=student,
                topic=topic,
                content_type=content_type,
                prompt_version=version,
                use_cache=use_cache,
            )

        comparison_file = self.storage.save_comparison(
            student_id=student.id,
            topic=topic,
            content_type=content_type,
            comparison=comparison,
        )
        comparison["comparison_file"] = comparison_file
        return comparison


# Backward-compatible alias for existing imports.
Generator = ContentGenerator
