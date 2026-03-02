#core/generator.py
from openai import OpenAI
from typing import Dict, Any, Optional
import asyncio
from .student import Student
from .prompt_engine import PromptEngine
from storage.cache_manager import CacheManager
from storage.jason_handler import JasonHandler
import logging
from datetime import datetime
import os

class ContentGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.client = OpenAI(
            api_key=config["OPENAI_API_KEY"]
            organization=config.get("OPENAI_ORGANIZATION")
            base_url=config.get("OPENAI_BASE_URL")
            )
        self.model = config["STANDARD_MODEL"]
        self.fallback_model = config.get("FALLBACK_MODEL", "gpt-3.5-turbo")
        self.temperature = config.get("TEMPERATURE", 0.7)
        self.max_tokens = config.get("MAX_TOKENS", 2000)
        self.cache_manager = CacheManager(config)
        self.storage = JasonHandler(config)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def generate_content(self, student: Student, topic: str, type: str, user_cache: bool = True) -> Dict[str, Any]:
        """Gera conteúdo personalizado para um estudante com base em seu perfil e preferências."""
        cache_key = f"{student.id}_{topic}_{type}"
        if user_cache:
            cached_content = self.cache_manager.get(cache_key)
            if cached_content and user_cache:
                logging.info(f"Cache hit for {cache_key}")
                return cached_content
        
        logging.info(f"Cache miss for {cache_key}. Generating new content.")
        engine = PromptEngine(student, topic, type)
        prompts ={
            "context": engine.generate_context_prompt(),
            "exercise": engine.generate_exercise_prompt(),
            "reflection": engine.generate_reflection_prompt(),
            "visual": engine.generate_visual_prompt()
        }
        try:
            prompt = prompts.get(type)
            if not prompt:
                raise ValueError(f"Prompt type '{type}' not supported")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are an educational assistant."},
                          {"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            self.cache_manager.set(cache_key, content)
            self.storage.save_record({
                "student_id": student.id,
                "topic": topic,
                "type": content_type,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            })
            return content
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            return None

    async def Openai_Call(self, prompt: str) -> Optional[str]:
        """Faz uma chamada à API do OpenAI com tratamento de erros e fallback."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error with model {self.model}: {e}")
            if self.fallback_model and self.fallback_model != self.model:
                logging.info(f"Attempting fallback with model {self.fallback_model}")
                try:
                    response = await self.client.chat.completions.create(
                        model=self.fallback_model,
                        messages=[{"role": "system", "content": "You are an educational assistant."},
                                  {"role": "user", "content": prompt}]
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    logging.error(f"Error with fallback model {self.fallback_model}: {e}")
            return None

    async def generate_comparison(self, student: Student, topic: str, types: list) -> Dict[str, Any]:
        """Gera uma comparação entre diferentes tipos de conteúdo para o mesmo tópico."""
        results = {}
        for content_type in types:
            content = await self.generate_content(student, topic, content_type)
            if content:
                results[content_type] = content
        return results

    def comparsion_analyse(self, comparison: Dict[str, Any]) -> str:
        """Analisa os resultados da comparação e gera um resumo das diferenças e semelhanças."""
        analysis = "Comparison Analysis:\n"
        for content_type, content in comparison.items():
            analysis += f"\n--- {content_type} ---\n{content}\n"
        return analysis

