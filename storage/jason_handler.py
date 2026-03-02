# storage/json_handler.py
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import hashlib
import uuid

class JSONHandler:
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = Path(base_dir)
        self.students_dir = self.base_dir / "students"
        self.record_dir = self.base_dir / "record"
        self._create_dir()
    
    def _create_dir(self):
        """Cria diretórios necessários"""
        self.students_dir.mkdir(parents=True, exist_ok=True)
        self.record_dir.mkdir(parents=True, exist_ok=True)

    
    def save_students(self, students: List[Dict]) -> str:
        """Salva lista de alunos em arquivo timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.students_dir / f"students_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "students_total": len(students),
            "students": students
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filename)
    
    def save_generation(self, student_id: str, topic: str, content_type: str, 
                       prompt: str, response: str, model: str) -> str:
        """Salva cada geração de conteúdo para histórico"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_id = hashlib.md5(f"{student_id}{topic}{timestamp}".encode()).hexdigest()[:8]
        filename = self.record_dir / f"{student_id}_{timestamp}_{hash_id}.json"
        
        data = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "student_id": student_id,
            "topic": topic,
            "content_type": content_type,
            "model": model,
            "prompt": prompt,
            "response": response,
            "metadata": {
                "versao": "1.0"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filename)
    
    def load_recent_students(self) -> List[Dict]:
        """Carrega a lista mais recente de alunos"""
        archives = sorted(self.students_dir.glob("students_*.json"), reverse=True)
        if not archives:
            return self._create_example_students()
        
        with open(archives[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["students"]
    
    def _create_example_students(self) -> List[Dict]:
        """Cria 5 alunos exemplo"""
        students_example = [
            {
                "id": "1",
                "name": "Ana Silva",
                "age": 8,
                "level": "iniciante",
                "style": "visual",
                "interests": ["animais", "desenho"]
            },
            {
                "id": "2",
                "name": "João Santos",
                "age": 15,
                "level": "intermediario",
                "style": "cinestesico",
                "interests": ["esportes", "videogame"]
            },
            {
                "id": "3",
                "name": "Maria Oliveira",
                "age": 25,
                "level": "avancado",
                "style": "leitura-escrita",
                "interests": ["programação", "ciência"]
            },
            {
                "id": "4",
                "name": "Pedro Costa",
                "age": 35,
                "level": "intermediario",
                "style": "auditivo",
                "interests": ["música", "história"]
            },
            {
                "id": "5",
                "name": "Lucia Pereira",
                "age": 45,
                "level": "iniciante",
                "style": "visual",
                "interests": ["jardinagem", "culinária"]
            }
        ]
        
        self.save_students(students_example)
        return students_example
    
    def obter_historico_analises(self, student_id: str = None) -> List[Dict]:
        """Obtém histórico para análises"""
        records = []
        for arquivo in self.record_dir.glob("*.json"):
            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if student_id is None or data["student_id"] == student_id:
                    records.append(data)
        
        return sorted(records, key=lambda x: x["timestamp"], reverse=True)
