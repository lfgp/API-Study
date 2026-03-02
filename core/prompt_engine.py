# core/prompt_engine.py
from typing import Dict, Any
from .student import Student
import json

class PromptEngine:
    def __init__(self, student: Student, topic: str):
        self.student = student
        self.topic = topic
        
    def generate_conceptual_prompt(self) -> list[Dict[str, str]]:
        """Prompt para explicação conceitual com Chain-of-Thought"""
        return [
            {"role": "system", "content": self.student.generate_persona_prompt()},
            {"role": "user", "content": f"""
            {self.student.contentgenerator(self.topic)}
            
            Por favor, forneça uma explicação conceitual seguindo este formato:
            
            1. **Contextualização**: Por que este tópico é importante?
            2. **Conceito Fundamental**: Explique de forma simples
            3. **Detalhamento**: Aprofunde gradualmente
            4. **Conexões**: Relacione com conhecimentos prévios
            5. **Analogia**: Crie uma analogia adequada à idade do aluno
            
            Use linguagem adequada para {self.student.style} e idade {self.student.age} anos.
            """}
        ]
    
    def generate_examples_prompt(self) -> list[Dict[str, str]]:
        """Prompt para exemplos práticos contextualizados"""
        return [
            {"role": "system", "content": self.student.generate_persona_prompt()},
            {"role": "user", "content": f"""
            {self.student.contentgenerator(self.topic)}
            
            Crie 3 exemplos práticos sobre {self.topic}:
            
            1. **Exemplo Cotidiano**: Algo do dia a dia do aluno
            2. **Exemplo Profissional/Lúdico**: Dependendo da idade
            3. **Exemplo Desafiador**: Que estimule o pensamento
            
            Para cada exemplo:
            - Contextualize a situação
            - Mostre a aplicação do conceito
            - Explique passo a passo o raciocínio
            
            Adapte a complexidade para nível {self.student.level}.
            """}
        ]
    
    def generate_reflection_prompt(self) -> list[Dict[str, str]]:
        """Prompt para perguntas de reflexão com CoT"""
        return [
            {"role": "system", "content": self.student.generate_persona_prompt()},
            {"role": "user", "content": f"""
            {self.student.contentgenerator(self.topic)}
            
            Crie 5 perguntas de reflexão sobre {self.topic}:
            
            - 2 perguntas básicas para verificar compreensão
            - 2 perguntas de aplicação prática
            - 1 pergunta desafiadora para pensamento crítico
            
            Para cada pergunta, inclua:
            * A pergunta em si
            * Dica para ajudar no raciocínio
            * Resposta esperada (para o tutor)
            
            As perguntas devem considerar o estilo {self.aluno.estilo}.
            """}
        ]
    
    def generate_visual_prompt(self) -> list[Dict[str, str]]:
        """Prompt para representação visual/diagrama"""
        return [
            {"role": "system", "content": self.student.generate_persona_prompt()},
            {"role": "user", "content": f"""
            {self.student.contentgenerator(self.topic)}
            
            Crie uma representação visual do conceito {self.topic}:
            
            1. **Diagrama ASCII**: Crie um diagrama usando caracteres ASCII
            2. **Descrição Visual**: Descreva como seria uma imagem/infográfico
            3. **Mapa Mental**: Estruture os conceitos em formato de mapa mental
            4. **Cores e Formas**: Sugira cores e formas que facilitariam o aprendizado
            
            Para estilo {self.student.style}, priorize:
            - Visual: Foque em diagramas e descrições visuais ricas
            - Auditivo: Descreva sons e ritmos associados
            - Leitura-Escrita: Use metáforas textuais elaboradas
            - Cinestésico: Associe a movimentos e sensações físicas
            
            Formato do diagrama deve ser legível em terminal.
            """}
        ]
