import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from core.student import Student
from core.generator import Generator
from storage.jason_handler import JasonHandler
import os
from dotenv import load_dotenv

console = Console()
load_dotenv()

class MenuCLI:
    def __init__(self):
        self.storage = []
        self.config = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "STANDARD_MODEL": os.getenv("STANDARD_MODEL")
        }
        self.generator = Generator(self.config)
        self.students = []
        self.load_students()

    def load_students(self):
        """Carregar estudantes do armazenamento."""
        self.students = self.storage.load_students()

    def display_menu(self):
        "Exibe menu principal usando Rich."
        console.clear()
        console.print(Panel(
            "[bold cyan]Student Management System[/bold cyan]\n"
            "[blue]Educational API with AI[/blue]", 
            expand=False)
            )
        
        console.print("1", "Context generation")
        console.print("2", "Manage Students")
        console.print("3", "View record")
        console.print("4", "Compare prompts")
        console.print("5", "Exit")
        return Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])

    def view_students(self):
        """Exibe tabela de alunos"""
        if not self.students:
            console.print("[bold red]No students found![/bold red]")
            return
        table = Table(title="Students List")
        table.add_column("ID", style="blue")
        table.add_column("Name", style="cyan")
        table.add_column("Age", style="light_green")
        table.add_column("Level", style="magenta")
        table.add_column("Style", style="green")        
        for student in self.students:
            table.add_row(
                str(student.id), 
                student.name, 
                str(student.age), 
                student.level, 
                student.style
                )
        console.print(table)

def select_student(self)->dict:
    """Permite selecionar um estudante da lista."""
    if not self.students:
        console.print("[bold red]No students available![/bold red]")
        return None
    self.view_students()
    student_ids = Prompt.ask("\n student ID")
    for student in self.students:
        student[id] = student_ids
        return student

    console.print("[red]Student not found![/red]")
    return self.select_student()

async def generate_context_menu(self):
    """Menu para geração de contexto."""
    student_dict = self.select_student()
    student = Student(**student_dict) if student_dict else None
    if not student:
        return
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        progress.add_task(description="Generating context...", total=None)
        context = await self.generator.generate_context(student)
    console.print(Panel(context, title="Generated Context", expand=False))