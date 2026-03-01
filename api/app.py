from flask import Flask, app, request, jsonify
from flask_cors import CORS
from core.student import Student
from core.generator import ContentGenerator
from storage.jason_handler import JSONHandler
import asyncio
from dotenv import load_dotenv
import os
from functools import wraps

load_dotenv()

config = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "STANDARD_MODEL": os.getenv("STANDARD_MODEL")
}

generator = ContentGenerator(config)
storage = JSONHandler()

def async_route(f):
    "Decorator para permitir rotas assíncronas no Flask"
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

@app.route('/api/students', methods=['GET'])
def students_list():
    "Retorna a lista de estudantes cadastrados"
    students = storage.load_students()
    return jsonify([s.dict() for s in students])

@app.route('/api/students', methods=['POST'])
def create_student():
    "Cria um novo estudante a partir dos dados enviados"
    data = request.json
    try:
        student = Student(**data)
        students = storage.load_students()
        students.append(student.dict())
        storage.save_students(students)
        return jsonify(student.dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/generate', methods=['POST'])
@async_route
async def generate_content():
    "Gera conteúdo personalizado para um estudante"
    data = request.json
    if not all(k in data for k in ['student_id','topic','type']):
        return jsonify({"error": "Dados incompletos"}), 400
    
    student = storage.load_student()
    student.dict = next((s for s in student if s['id'] == data['student_id']), None)
    if not student:
        return jsonify({"error": "Estudante não encontrado"}), 404

    try:
        student = Student(**data)
        valid_types = ['conceptual', 'examples', 'reflection','visual']
        if data['type'] not in valid_types:
            return jsonify({"error": f"Tipo inválido. Tipos válidos: {valid_types}"}), 400
        
        content = await generator.content_generate(
            student=student,
            topic=data['topic'],
            type=data['type'],
            use_cache=data.get('use_cache', True)
        )
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/compare', methods=['POST'])
@async_route
async def compare_prompts():
    "Compara dois conteúdos gerados para o mesmo tópico"
    data = request.json
    if not all(k in data for k in ['student_id','topic']):
        return jsonify({"error": "Dados incompletos"}), 400
    
    student = storage.load_student()
    student.dict = next((s for s in student if s['id'] == data['student_id']), None)
    if not student:
        return jsonify({"error": "Estudante não encontrado"}), 404

    try:
        student = Student(**student.dict)
        types = data.get('types', ['conceptual', 'examples', 'reflection','visual'])
    
        comparison = generator.generate_comparison(student=student, topic=data['topic'], types=types)
        return jsonify(comparison)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/record', methods=['POST'])
@async_route
async def record():
    "Retorna o histórico de interações de um estudante"
    student_id = request.json.get('student_id')
    limit = int(request.json.get('limit', 100))
    record = storage.get_record_analysis(student_id=student_id, limit=limit)
    return jsonify({
        "total": len(record), 
        "record": record[:limit]
        })

@app.route('/api/analysis/styles', methods=['POST'])
@async_route            
async def analysis_styles():
    "Análise dos estilos de aprendizagem de um estudante com base em suas interações"
    record = storage.get_record_analysis()
    styles = {}
    for item in record:
        style = item.get('student', {}).get('style','unknown')
        if style not in styles:
            styles[style] = 0
        styles[style] += 1

    return jsonify({
        "styles_distribuiton": styles,
        "total_versions": len(record)
        })

if __name__ == '__main__':
    app.run(debug=True,port=5000)