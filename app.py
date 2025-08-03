from flask import Flask, request, jsonify
from flask_cors import CORS
from models import TodoRepository

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Instance du repository pour gérer les données
todo_repo = TodoRepository()

# Données de test
def init_sample_data():
    """Initialise quelques tâches en dur"""
    todo_repo.create_todo("Apprendre Python", "Créer une API REST avec Flask")
    todo_repo.create_todo("Faire les courses", "Acheter des légumes et des fruits")
    todo_repo.create_todo("Courir lundi", "Faire course de 5km")

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return jsonify({'status': 'healthy', 'message': 'Todo API is running'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    """Récupère toutes les tâches avec filtrage optionnel"""
    status = request.args.get('status')  # Paramètre optionnel: completed, pending

    if status == 'completed':
        todos = todo_repo.get_completed_todos()
    elif status == 'pending':
        todos = todo_repo.get_pending_todos()
    else:
        todos = todo_repo.get_all_todos()

    return jsonify({
        'todos': [todo.to_dict() for todo in todos],
        'count': len(todos)
    }), 200

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id: int):
    """Récupère une tâche spécifique par son ID"""
    todo = todo_repo.get_todo_by_id(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify(todo.to_dict()), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    """Crée une nouvelle tâche"""
    data = request.get_json()

    # Validation des données
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    if not data['title'].strip():
        return jsonify({'error': 'Title cannot be empty'}), 400

    # Création de la tâche
    todo = todo_repo.create_todo(
        title=data['title'].strip(),
        description=data.get('description', '').strip()
    )

    return jsonify(todo.to_dict()), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id: int):
    """Met à jour une tâche existante"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validation: au moins un champ doit être fourni
    allowed_fields = ['title', 'description', 'completed']
    if not any(field in data for field in allowed_fields):
        return jsonify({'error': 'At least one field (title, description, completed) must be provided'}), 400

    # Validation du titre s'il est fourni
    if 'title' in data and not data['title'].strip():
        return jsonify({'error': 'Title cannot be empty'}), 400

    # Mise à jour
    todo = todo_repo.update_todo(
        todo_id=todo_id,
        title=data.get('title', '').strip() if 'title' in data else None,
        description=data.get('description', '').strip() if 'description' in data else None,
        completed=data.get('completed') if 'completed' in data else None
    )

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify(todo.to_dict()), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id: int):
    """Supprime une tâche"""
    success = todo_repo.delete_todo(todo_id)

    if not success:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify({'message': 'Todo deleted successfully'}), 200

@app.route('/todos/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id: int):
    """Inverse le statut completed d'une tâche"""
    todo = todo_repo.get_todo_by_id(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    updated_todo = todo_repo.update_todo(todo_id, completed=not todo.completed)

    return jsonify(updated_todo.to_dict()), 200

@app.route('/todos/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques des tâches"""
    all_todos = todo_repo.get_all_todos()
    completed = todo_repo.get_completed_todos()
    pending = todo_repo.get_pending_todos()

    return jsonify({
        'total': len(all_todos),
        'completed': len(completed),
        'pending': len(pending),
        'completion_rate': len(completed) / len(all_todos) * 100 if all_todos else 0
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialisation des données de test
    init_sample_data()

    # Lancement du serveur en mode debug
    print("🚀 Starting Todo API...")
    print("📍 API available at: http://localhost:8080")
    print("🔍 Health check: http://localhost:8080/health")
    print("📝 Todos endpoint: http://localhost:8080/todos")

    app.run(debug=True, host='0.0.0.0', port=8080)