from __future__ import annotations

from typing import Dict, List

from .student import Student


CONTENT_TYPES = ("conceptual", "examples", "reflection", "visual")
PROMPT_VERSIONS = ("v1", "v2")


class PromptEngine:
    def __init__(self, student: Student, topic: str, prompt_version: str = "v1"):
        if prompt_version not in PROMPT_VERSIONS:
            raise ValueError(f"Invalid prompt_version '{prompt_version}'. Use one of: {PROMPT_VERSIONS}")
        self.student = student
        self.topic = topic
        self.prompt_version = prompt_version

    def build_messages(self, content_type: str) -> List[Dict[str, str]]:
        if content_type not in CONTENT_TYPES:
            raise ValueError(f"Invalid content_type '{content_type}'. Use one of: {CONTENT_TYPES}")

        user_prompt = {
            "conceptual": self._conceptual_prompt(),
            "examples": self._examples_prompt(),
            "reflection": self._reflection_prompt(),
            "visual": self._visual_prompt(),
        }[content_type]

        return [
            {"role": "system", "content": self.student.build_persona_prompt()},
            {"role": "user", "content": user_prompt},
        ]

    def _base_context(self) -> str:
        style_hint = (
            f"Adapte linguagem e profundidade para idade {self.student.age}, "
            f"nivel {self.student.level.value} e estilo {self.student.style.value}."
        )
        version_hint = (
            "Use resposta objetiva em blocos curtos."
            if self.prompt_version == "v1"
            else "Use resposta um pouco mais detalhada, com mini-checklist no final."
        )
        return f"{self.student.build_student_context(self.topic)}\n{style_hint}\n{version_hint}"

    def _conceptual_prompt(self) -> str:
        return f"""
{self._base_context()}

Tarefa: Gerar EXPLICACAO CONCEITUAL sobre "{self.topic}".
Use chain-of-thought internamente: pense passo a passo antes de responder.
Formato obrigatorio:
1) Contextualizacao (por que importa)
2) Conceito central (simples)
3) Explicacao progressiva (do basico ao avancado)
4) Conexao com algo que o estudante ja conhece
5) Analogia adequada para a idade
""".strip()

    def _examples_prompt(self) -> str:
        return f"""
{self._base_context()}

Tarefa: Gerar EXEMPLOS PRATICOS sobre "{self.topic}".
Formato obrigatorio:
- Exemplo 1: cotidiano
- Exemplo 2: interesse do estudante
- Exemplo 3: situacao de desafio
Para cada exemplo, inclua: contexto, aplicacao do conceito e passo a passo.
""".strip()

    def _reflection_prompt(self) -> str:
        return f"""
{self._base_context()}

Tarefa: Gerar PERGUNTAS DE REFLEXAO sobre "{self.topic}".
Formato obrigatorio:
- 2 perguntas de compreensao
- 2 perguntas de aplicacao
- 1 pergunta de pensamento critico
Para cada pergunta, inclua: pergunta, dica curta e resposta esperada para o tutor.
""".strip()

    def _visual_prompt(self) -> str:
        return f"""
{self._base_context()}

Tarefa: Gerar RESUMO VISUAL sobre "{self.topic}".
Formato obrigatorio:
1) Diagrama ASCII legivel em terminal
2) Mini-mapa mental em texto
3) Breve explicacao de como interpretar o diagrama
""".strip()
