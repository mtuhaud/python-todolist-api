from flask import Flask, request, jsonify
from flask_cors import CORS
from models import TodoRepository, DatabaseManager

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Configuration pour l'affichage correct des caractères UTF-8
app.config['JSON_AS_ASCII'] = False

# Initialisation de la base de données et du repository
db_manager = DatabaseManager()
todo_repo = TodoRepository(db_manager)

# Données de test
def init_sample_data():
    """Initialise quelques tâches de démonstration si la BDD est vide"""
    existing_todos = todo_repo.get_all_todos()

    if not existing_todos:  # Seulement si aucune tâche n'existe
        print("📝 Initialisation des données de test...")
        todo_repo.create_todo("Apprendre Python", "Créer une API REST avec Flask")
        todo_repo.create_todo("Faire les courses", "Acheter des légumes et des fruits")
        todo_repo.create_todo("Courir mardi", "Faire course de 5km")
        print("✅ Données de test créées")
    else:
        print(f"📊 {len(existing_todos)} tâches déjà présentes en base")

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'message': 'Todo API is running',
        'database': 'SQLite connected'
    }), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    """Récupère toutes les tâches avec filtrage optionnel"""
    try:
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

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération: {str(e)}'}), 500

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id: int):
    """Récupère une tâche spécifique par son ID"""
    try:
        todo = todo_repo.get_todo_by_id(todo_id)

        if not todo:
            return jsonify({'error': 'Todo not found'}), 404

        return jsonify(todo.to_dict()), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération: {str(e)}'}), 500

@app.route('/todos', methods=['POST'])
def create_todo():
    """Crée une nouvelle tâche"""
    try:
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

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la création: {str(e)}'}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id: int):
    """Met à jour une tâche existante"""
    try:
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

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la mise à jour: {str(e)}'}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id: int):
    """Supprime une tâche"""
    try:
        success = todo_repo.delete_todo(todo_id)

        if not success:
            return jsonify({'error': 'Todo not found'}), 404

        return jsonify({'message': 'Todo deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500

@app.route('/todos/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id: int):
    """Inverse le statut completed d'une tâche"""
    try:
        todo = todo_repo.get_todo_by_id(todo_id)

        if not todo:
            return jsonify({'error': 'Todo not found'}), 404

        updated_todo = todo_repo.update_todo(todo_id, completed=not todo.completed)

        return jsonify(updated_todo.to_dict()), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors du basculement: {str(e)}'}), 500

@app.route('/todos/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques des tâches"""
    try:
        counts = todo_repo.count_todos()

        return jsonify({
            'total': counts['total'],
            'completed': counts['completed'],
            'pending': counts['pending'],
            'completion_rate': counts['completed'] / counts['total'] * 100 if counts['total'] > 0 else 0
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors du calcul des statistiques: {str(e)}'}), 500

# Endpoint bonus pour la gestion de la BDD
@app.route('/admin/reset', methods=['POST'])
def reset_database():
    """Reset de la base de données (utile pour les tests)"""
    try:
        db_manager.drop_all_tables()
        db_manager.create_tables()
        init_sample_data()

        return jsonify({'message': 'Base de données réinitialisée avec succès'}), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors du reset: {str(e)}'}), 500

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

    print("🚀 Starting Todo API with SQLite...")
    print("📍 API available at: http://localhost:8080")
    print("🔍 Health check: http://localhost:8080/health")
    print("📝 Todos endpoint: http://localhost:8080/todos")
    print("📊 Stats endpoint: http://localhost:8080/todos/stats")
    print("🗄️ Database: SQLite (todos.db)")

    app.run(debug=True, host='0.0.0.0', port=8080)