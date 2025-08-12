# 📝 Python Todo API avec Flask + SQLite

> **Contexte** : Projet réalisé pour découvrir Python, Flask et SQLAlchemy.

## 🎯 Objectifs du projet

- Apprendre les bases de Python et Flask
- Découvrir SQLAlchemy (ORM Python équivalent JPA/Hibernate)
- Utiliser SQLite comme base de données intégrée (équivalent H2)
- Créer une API REST fonctionnelle avec persistance

## 🛠️ Technologies utilisées

- **Python 3.x** - Langage principal
- **Flask** - Framework web minimaliste
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **SQLite** - Base de données intégrée (comme H2 en Java)
- **Flask-CORS** - Gestion des requêtes cross-origin

## 🗄️ Base de données

- **SQLite** : Base de données intégrée (fichier `todos.db`)
- **Auto-création** des tables au démarrage
- **Migrations** automatiques via SQLAlchemy
- **Données de test** initialisées si la BDD est vide

## 📋 Fonctionnalités

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Vérification de santé de l'API |
| `GET` | `/todos` | Récupère toutes les tâches |
| `GET` | `/todos?status=pending` | Récupère les tâches en cours |
| `GET` | `/todos?status=completed` | Récupère les tâches terminées |
| `GET` | `/todos/{id}` | Récupère une tâche spécifique |
| `POST` | `/todos` | Crée une nouvelle tâche |
| `PUT` | `/todos/{id}` | Met à jour une tâche |
| `DELETE` | `/todos/{id}` | Supprime une tâche |
| `PATCH` | `/todos/{id}/toggle` | Inverse le statut d'une tâche |
| `GET` | `/todos/stats` | Récupère les statistiques |
| `POST` | `/admin/reset` | Remet à zéro la BDD (dev uniquement) |

### Structure d'une tâche

```json
{
  "id": 1,
  "title": "Apprendre Python",
  "description": "Créer une API REST avec Flask",
  "completed": false,
  "created_at": "2025-08-03T10:30:00",
  "updated_at": "2025-08-03T10:30:00"
}
```

## 🚀 Installation et lancement

### Prérequis
- Python 3.x installé
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet**
```bash
git clone https://github.com/mtuhaud/python-todolist-api.git
cd python-todolist-api
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# ou
venv\Scripts\activate     # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt

# Ou installer manuellement
pip install flask flask-cors sqlalchemy
```

4. **Lancer l'application**
```bash
python app.py
```

L'API sera accessible sur `http://localhost:8080`

## 🧪 Tests manuels avec curl

### Créer une tâche
```bash
curl -X POST http://localhost:8080/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Ma nouvelle tâche", "description": "Description optionnelle"}'
```

### Récupérer toutes les tâches
```bash
curl http://localhost:8080/todos
```

### Marquer une tâche comme terminée
```bash
curl -X PUT http://localhost:8080/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Voir les statistiques
```bash
curl http://localhost:8080/todos/stats
```

## 🏗️ Architecture du projet

```
python-todo-api/
├── app.py              # Point d'entrée et routes Flask
├── models.py           # Modèles SQLAlchemy et logique d'accès aux données
├── requirements.txt    # Dépendances Python
├── todos.db           # Base de données SQLite (créé automatiquement)
└── README.md          # Documentation
```

## 💡 Concepts Python/SQLAlchemy découverts

- **SQLAlchemy ORM** : Équivalent Python de JPA/Hibernate
- **Déclarative Base** : Définition des modèles comme en JPA
- **Sessions** : Gestion des transactions (comme EntityManager)
- **Context Managers** : `with session` pour la gestion automatique des ressources
- **Type hints** : Amélioration de la lisibilité du code
- **Décorateurs Flask** : Système de routes élégant
- **Gestion des erreurs** : Try/catch et gestionnaires d'erreurs globaux
