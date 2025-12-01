# 🔗 Intégration Microservice Student Service

## Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Django API    │◄──────────────►│  Spring Boot    │
│  (Course Service)│                │ (Student Service)│
│   Port: 8000    │                │   Port: 8080     │
└─────────────────┘                └─────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                ┌─────────────────┐
│   SQLite DB     │                │   MySQL DB      │
│   (Courses)     │                │   (Students)    │
└─────────────────┘                └─────────────────┘
```

## Configuration

### 1. Django Settings (course_service/settings.py)
```python
# Configuration du microservice Student Service
STUDENT_SERVICE_URL = 'http://localhost:8080/api/students'
STUDENT_SERVICE_TIMEOUT = 5  # Timeout en secondes
```

## Endpoints

### 🎓 Validation des étudiants
```
GET /api/students/validate/{student_id}/
```
**Exemple :** `GET /api/students/validate/123/`

**Réponse si étudiant valide :**
```json
{
    "message": "✅ Student is valid",
    "student_info": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

### 📚 Inscription d'un étudiant à un cours
```
POST /api/studentcourse/add/
```
**Body :**
```json
{
    "student_id": 123,
    "course": 1
}
```

**Réponse :**
```json
{
    "message": "✅ Student added to course successfully!",
    "student_info": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "enrollment": {
        "id": 1,
        "student_id": 123,
        "course": 1
    }
}
```

### 📖 Récupérer les cours d'un étudiant
```
GET /api/studentcourses/by_student/?student_id=123
```

**Réponse :**
```json
{
    "student_info": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "enrollments": [
        {
            "id": 1,
            "student_id": 123,
            "course": {
                "id": 1,
                "name": "Python Programming",
                "instructor": "Dr. Sara",
                "category": "Programming"
            }
        }
    ],
    "total_courses": 1
}
```

## Gestion des erreurs

### ❌ Étudiant non trouvé
```json
{
    "error": "❌ Student validation failed: Student not found",
    "student_id": 123
}
```

### ❌ Service Student indisponible
```json
{
    "error": "❌ Student validation failed: Student service unavailable",
    "student_id": 123
}
```

### ❌ Étudiant déjà inscrit
```json
{
    "error": "❌ Student is already enrolled in this course",
    "student_id": 123,
    "course_id": 1
}
```

## Configuration du Spring Boot Service

Votre microservice Student Service (Spring Boot) doit exposer ces endpoints :

### 1. Récupérer un étudiant par ID
```
GET /api/students/{id}
```

**Réponse attendue :**
```json
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "department": "Computer Science"
}
```

**Codes de statut :**
- `200` : Étudiant trouvé
- `404` : Étudiant non trouvé
- `500` : Erreur serveur

## Tests

### 1. Test de validation d'étudiant
```bash
curl -X GET "http://localhost:8000/api/students/validate/123/"
```

### 2. Test d'inscription à un cours
```bash
curl -X POST "http://localhost:8000/api/studentcourse/add/" \
  -H "Content-Type: application/json" \
  -d '{"student_id": 123, "course": 1}'
```

### 3. Test de récupération des cours d'un étudiant
```bash
curl -X GET "http://localhost:8000/api/studentcourses/by_student/?student_id=123"
```

## Logs et monitoring

Les logs sont disponibles dans la console Django pour :
- ✅ Appels réussis vers le Student Service
- ❌ Erreurs de connexion
- ⏱️ Timeouts
- 🔍 Détails des validations

## Déploiement

1. **Démarrer le Student Service (Spring Boot)** sur le port 8080
2. **Démarrer le Course Service (Django)** sur le port 8000
3. **Tester la communication** avec les endpoints ci-dessus

## Sécurité

Pour la production, considérez :
- 🔐 Authentification entre services (JWT, API Keys)
- 🛡️ HTTPS pour les communications
- 🔒 Validation des données d'entrée
- 📊 Rate limiting
