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

    console.print(f"\n[bold green]Selected student:[/bold green] {student.name}")
    prompt = Prompt.ask("Enter a topic for context generation")

    console.print(f"\n[bold green]Generating context for topic:[/bold green] {prompt}")
    topic = prompt.ask("Enter a topic for context generation")

    console.print("\n[bold green]Topic type:[/bold green]")
    console.print("1", "Contextual explanation")
    console.print("2", "Practical examples")
    console.print("3", "Reflection questions")
    console.print("4", "Interactive exercises")
    console.print("5", "Personalized feedback")
    console.print("6", "Adaptive learning paths")
    console.print("7", "Gamification elements")
    console.print("8", "Real-world applications")
    console.print("9", "Collaborative learning prompts")
    console.print("10", "Multimodal content suggestions")
    console.print("11", "Cultural and historical context")
    console.print("12", "All of the above")

    map_types = {
        "1": "Contextual explanation", 
        "2": "Practical examples",
        "3": "Reflection questions",
        "4": "Interactive exercises",
        "5": "Personalized feedback",
        "6": "Adaptive learning paths",
        "7": "Gamification elements",
        "8": "Real-world applications",
        "9": "Collaborative learning prompts",
        "10": "Multimodal content suggestions",
        "11": "Cultural and historical context",
        "12": "All of the above"}

    option = Prompt.ask("Select a topic type", choices=[str(i) for i in range(1, 13)])

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        progress.add_task(description="Generating context...", total=None)
        context = await self.generator.generate_context(student, topic, map_types[option])

    if option == "12":
        console.print(Panel(context, title="Generated Context (All Types)", expand=False))
        """Gera todos os tipos de contexto e exibe em um painel separado para cada tipo."""
        types = [
            "Contextual explanation", 
            "Practical examples",
            "Reflection questions",
            "Interactive exercises",
            "Personalized feedback",
            "Adaptive learning paths",
            "Gamification elements",
            "Real-world applications",
            "Collaborative learning prompts",
            "Multimodal content suggestions",
            "Cultural and historical context"
        ]
        for type in types:
            result = await self.generator.generate_context(student, topic, type)
            self.result_exibition(result)

            else:
                type = map_types[option]
                result = await self.generator.generate_context(student, topic, type)
                self.result_exibition(result)

        input("\nPress Enter to return to the main menu...")

    def result_exibition(self, result:dict):
        """Exibe o resultado em um painel formatado."""
        console.print(f"\n[bold green]Generated context for topic:[/bold green] {result['topic']} - [bold magenta]{result['type']}[/bold magenta]")
        console.print(Panel(result, title="Generated Context", expand=False))
        console.print(f"\n[dim]Model: {result['model']} [/dim]")
        console.print(f"\n[dim]Generated at: {result['timestamp']} [/dim]")

    async def menu_comparsion(self):
        """Menu para comparação de prompts."""
        student_dict = self.select_student()
        student = Student(**student_dict) if student_dict else None
        if not student:
            return

        topic = Prompt.ask("Enter a topic for comparsion")

        console.print("\n[bold green]Select prompt types to compare:[/bold green]")
        console.print("1", "Contextual vs Examples")
        console.print("2", "Reflection vs Interactive")
        console.print("3", "Personalized vs Adaptive")
        console.print("4", "Gamification vs Real-world")
        console.print("5", "All of the above")

        option = Prompt.ask("Select an option", choices=[str(i) for i in range(1, 6)])

        map_comparisons = {
            "1": ("Contextual explanation", "Practical examples"),
            "2": ("Reflection questions", "Interactive exercises"),
            "3": ("Personalized feedback", "Adaptive learning paths"),
            "4": ("Gamification elements", "Real-world applications"),
            "5": "All of the above"
            }

        comparsions = map_comparisons[option]
        With Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(description="Generating contexts for comparison...", total=None)
        comparsion_results = await self.generator.compare_prompts(student, topic, comparsions)

        for comparsions, result in comparsion_results[results].items():
            self.result_exibition(result)
            progress.advance(task)

        input("\nPress Enter to return to the main menu...")

    async def run(self):
        """Loop principal do menu."""
        while True:
            choice = self.display_menu()
            if choice == "1":
                await self.generate_context_menu()
            elif choice == "2":
                self.view_students()
                input("\nPress Enter to return to the main menu...")
            elif choice == "3":
                console.print("[bold yellow]View record feature coming soon![/bold yellow]")
                input("\nPress Enter to return to the main menu...")
            elif choice == "4":
                await self.menu_comparsion()
            elif choice == "5":
                console.print("[bold cyan]Goodbye![/bold cyan]")
                break

    def main():
        menu = MenuCLI()
        asyncio.run(menu.run())

    if __name__ == "__main__":
        main()
