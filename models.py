from datetime import datetime
from typing import List, Optional, Dict, Any

class Todo:
    """Modèle représentant une tâche todo"""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet Todo en dictionnaire pour la sérialisation JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, title: Optional[str] = None, description: Optional[str] = None,
               completed: Optional[bool] = None):
        """Met à jour les champs de la tâche"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now()

class TodoRepository:
    """Repository pour gérer les opérations CRUD sur les todos"""

    def __init__(self):
        self.todos: List[Todo] = []
        self.next_id = 1

    def create_todo(self, title: str, description: str = "") -> Todo:
        """Crée une nouvelle tâche"""
        todo = Todo(self.next_id, title, description)
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def get_all_todos(self) -> List[Todo]:
        """Récupère toutes les tâches"""
        return self.todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Récupère une tâche par son ID"""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        """Met à jour une tâche existante"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.update(title, description, completed)
            return todo
        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Supprime une tâche"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self.todos.remove(todo)
            return True
        return False

    def get_completed_todos(self) -> List[Todo]:
        """Récupère toutes les tâches terminées"""
        return [todo for todo in self.todos if todo.completed]

    def get_pending_todos(self) -> List[Todo]:
        """Récupère toutes les tâches en cours"""
        return [todo for todo in self.todos if not todo.completed]