from __future__ import annotations

import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from core.generator import ContentGenerator
from core.prompt_engine import CONTENT_TYPES
from core.student import Student
from storage.jason_handler import JSONHandler


load_dotenv()
console = Console()


class MenuCLI:
    def __init__(self) -> None:
        self.config = {
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
        self.storage = JSONHandler(self.config["DATA_DIR"])
        self.generator = ContentGenerator(self.config)

    def display_menu(self) -> str:
        console.print(Panel("API Study - Menu CLI", expand=False))
        console.print("1. List students")
        console.print("2. Generate 4 content types")
        console.print("3. Compare prompt versions")
        console.print("4. View generation history")
        console.print("5. Exit")
        return Prompt.ask("Choose", choices=["1", "2", "3", "4", "5"])

    def list_students(self) -> None:
        students = self.storage.load_students()
        table = Table(title="Students")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Age")
        table.add_column("Level")
        table.add_column("Style")
        for student in students:
            table.add_row(
                str(student.get("id", "")),
                str(student.get("name", "")),
                str(student.get("age", "")),
                str(student.get("level", "")),
                str(student.get("style", "")),
            )
        console.print(table)

    def select_student(self) -> Optional[Student]:
        students = self.storage.load_students()
        if not students:
            console.print("No students found.")
            return None

        self.list_students()
        student_id = Prompt.ask("Student ID")
        student_data = self.storage.get_student_by_id(student_id)
        if not student_data:
            console.print("Student not found.")
            return None
        return Student(**student_data)

    async def generate_all(self) -> None:
        student = self.select_student()
        if not student:
            return

        topic = Prompt.ask("Topic")
        prompt_version = Prompt.ask("Prompt version", choices=["v1", "v2"], default="v1")

        result = await self.generator.generate_all_types(
            student=student,
            topic=topic,
            prompt_version=prompt_version,
            use_cache=True,
        )

        for content_type in CONTENT_TYPES:
            content = result["results"][content_type]["response"]
            console.print(Panel(content, title=f"{content_type} ({prompt_version})", expand=False))

        console.print(f"Bundle saved at: {result['bundle_file']}")

    async def compare_versions(self) -> None:
        student = self.select_student()
        if not student:
            return

        topic = Prompt.ask("Topic")
        content_type = Prompt.ask("Content type", choices=list(CONTENT_TYPES))

        comparison = await self.generator.compare_prompt_versions(
            student=student,
            topic=topic,
            content_type=content_type,
            versions=("v1", "v2"),
            use_cache=False,
        )

        for version, payload in comparison["versions"].items():
            console.print(Panel(payload["response"], title=f"{content_type} - {version}", expand=False))

        console.print(f"Comparison saved at: {comparison['comparison_file']}")

    def view_history(self) -> None:
        student_id = Prompt.ask("Student ID (optional)", default="").strip() or None
        history = self.storage.get_generation_history(student_id=student_id, limit=20)
        if not history:
            console.print("No history found.")
            return

        table = Table(title="Generation History (latest 20)")
        table.add_column("Timestamp")
        table.add_column("Student ID")
        table.add_column("Type")
        table.add_column("Prompt Ver")
        table.add_column("Cache")
        for item in history:
            table.add_row(
                str(item.get("timestamp", "")),
                str(item.get("student_id", "")),
                str(item.get("content_type", item.get("results", "bundle"))),
                str(item.get("prompt_version", "-")),
                str(item.get("used_cache", "-")),
            )
        console.print(table)

    async def run(self) -> None:
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.list_students()
            elif choice == "2":
                await self.generate_all()
            elif choice == "3":
                await self.compare_versions()
            elif choice == "4":
                self.view_history()
            elif choice == "5":
                break


def main() -> None:
    menu = MenuCLI()
    asyncio.run(menu.run())


if __name__ == "__main__":
    main()
