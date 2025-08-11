from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Base pour les modèles SQLAlchemy
Base = declarative_base()

class Todo(Base):
    """Modèle représentant une tâche todo avec persistance SQLAlchemy"""

    __tablename__ = 'todos'

    # Colonnes de la table
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), default="")
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

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

    def update_fields(self, title: Optional[str] = None, description: Optional[str] = None,
                      completed: Optional[bool] = None):
        """Met à jour les champs de la tâche"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now(timezone.utc)

class DatabaseManager:
    """Gestionnaire de la base de données SQLite"""

    def __init__(self, database_url: str = None):
        if database_url is None:
            # Base de données SQLite locale (équivalent H2)
            database_url = "sqlite:///todos.db"

        self.engine = create_engine(
            database_url,
            echo=False,  # Mettre True pour voir les requêtes SQL
            connect_args={"check_same_thread": False}  # Nécessaire pour SQLite + Flask
        )

        # Création du sessionmaker
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Création des tables si elles n'existent pas
        self.create_tables()

    def create_tables(self):
        """Crée toutes les tables définies dans Base"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """Retourne une nouvelle session de base de données"""
        return self.SessionLocal()

    def drop_all_tables(self):
        """Supprime toutes les tables (utile pour les tests)"""
        Base.metadata.drop_all(bind=self.engine)

class TodoRepository:
    """Repository pour gérer les opérations CRUD sur les todos avec SQLAlchemy"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_todo(self, title: str, description: str = "") -> Todo:
        """Crée une nouvelle tâche"""
        with self.db_manager.get_session() as session:
            todo = Todo(title=title, description=description)
            session.add(todo)
            session.commit()
            session.refresh(todo)  # Récupère l'ID généré
            return todo

    def get_all_todos(self) -> List[Todo]:
        """Récupère toutes les tâches"""
        with self.db_manager.get_session() as session:
            return session.query(Todo).order_by(Todo.created_at.desc()).all()

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Récupère une tâche par son ID"""
        with self.db_manager.get_session() as session:
            return session.query(Todo).filter(Todo.id == todo_id).first()

    def update_todo(self, todo_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        """Met à jour une tâche existante"""
        with self.db_manager.get_session() as session:
            todo = session.query(Todo).filter(Todo.id == todo_id).first()
            if todo:
                todo.update_fields(title, description, completed)
                session.commit()
                session.refresh(todo)
                return todo
            return None

    def delete_todo(self, todo_id: int) -> bool:
        """Supprime une tâche"""
        with self.db_manager.get_session() as session:
            todo = session.query(Todo).filter(Todo.id == todo_id).first()
            if todo:
                session.delete(todo)
                session.commit()
                return True
            return False

    def get_completed_todos(self) -> List[Todo]:
        """Récupère toutes les tâches terminées"""
        with self.db_manager.get_session() as session:
            return session.query(Todo).filter(Todo.completed == True).order_by(Todo.created_at.desc()).all()

    def get_pending_todos(self) -> List[Todo]:
        """Récupère toutes les tâches en cours"""
        with self.db_manager.get_session() as session:
            return session.query(Todo).filter(Todo.completed == False).order_by(Todo.created_at.desc()).all()

    def count_todos(self) -> Dict[str, int]:
        """Compte les tâches par statut"""
        with self.db_manager.get_session() as session:
            total = session.query(Todo).count()
            completed = session.query(Todo).filter(Todo.completed == True).count()
            pending = session.query(Todo).filter(Todo.completed == False).count()

            return {
                'total': total,
                'completed': completed,
                'pending': pending
            }