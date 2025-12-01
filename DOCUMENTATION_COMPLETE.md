# 📚 Documentation Complète du Projet Course Service

## 🎯 Vue d'ensemble du projet

Ce projet Django implémente un **service de gestion des cours** avec intégration microservice pour la validation des étudiants. Il utilise Django REST Framework pour créer une API REST complète.

## 🏗️ Architecture du projet

```
course_service/
├── course_service/          # Configuration principale Django
│   ├── settings.py         # Configuration du projet
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Point d'entrée WSGI
├── course/                 # Application principale
│   ├── models.py          # Modèles de données (tables)
│   ├── views.py           # Vues et logique métier
│   ├── serializers.py     # Conversion JSON ↔ Objets
│   ├── services.py        # Communication microservice
│   ├── urls.py           # Routes de l'application
│   └── admin.py          # Interface d'administration
└── db.sqlite3            # Base de données SQLite
```

## 📋 Fichiers du projet avec commentaires détaillés

### 1. **models.py** - Structure de la base de données
- **Course** : Modèle pour les cours (nom, instructeur, catégorie, horaire)
- **StudentCourse** : Table de liaison entre étudiants et cours
- **Relations** : ForeignKey entre StudentCourse et Course
- **Contraintes** : Unicité sur (student_id, course)

### 2. **views.py** - Logique métier et API
- **Fonctions CRUD** : add_course, get_all_courses, get_course_by_id, update_course, delete_course
- **Fonctions d'inscription** : add_student_to_course avec validation microservice
- **ViewSets** : CourseViewSet et StudentCourseViewSet avec filtrage automatique
- **Routes personnalisées** : by_student pour récupérer les cours d'un étudiant

### 3. **serializers.py** - Conversion de données
- **CourseSerializer** : Convertit les objets Course en JSON
- **StudentCourseSerializer** : Convertit les inscriptions avec champ calculé course_name
- **Validation** : Vérification automatique des données

### 4. **services.py** - Communication microservice
- **StudentService** : Classe pour communiquer avec le service Spring Boot
- **Gestion d'erreurs** : Timeout, connexion, erreurs serveur
- **Logging** : Enregistrement des erreurs et opérations
- **Configuration** : URL et timeout configurables

### 5. **urls.py** - Configuration des routes
- **Router automatique** : Génération des routes CRUD pour les ViewSets
- **Routes fonctionnelles** : Routes manuelles pour les fonctions
- **Routes de validation** : Endpoints pour valider les étudiants
- **Paramètres d'URL** : Capture des IDs et paramètres

### 6. **settings.py** - Configuration Django
- **Applications** : Django, REST Framework, django-filters, course
- **Base de données** : SQLite pour le développement
- **Sécurité** : Configuration de sécurité (développement)
- **Microservice** : Configuration URL et timeout du service externe

## 🔗 Intégration microservice

### Communication avec Spring Boot
```python
# Configuration dans settings.py
STUDENT_SERVICE_URL = 'http://localhost:8080/api/students'
STUDENT_SERVICE_TIMEOUT = 5
```

### Flux de validation
1. **Réception** : Données JSON dans la requête
2. **Validation** : Vérification des données avec le sérialiseur
3. **Appel microservice** : HTTP GET vers le service Spring Boot
4. **Vérification** : Contrôle de l'existence de l'étudiant
5. **Inscription** : Création de l'association si tout est valide

## 🛠️ Fonctionnalités implémentées

### Gestion des cours
- ✅ Création, lecture, modification, suppression
- ✅ Filtrage par instructeur, catégorie, nom
- ✅ Recherche textuelle dans plusieurs champs
- ✅ Validation des données

### Gestion des inscriptions
- ✅ Inscription d'étudiants aux cours
- ✅ Validation via microservice externe
- ✅ Vérification des doublons
- ✅ Récupération des cours d'un étudiant

### API REST complète
- ✅ Endpoints CRUD automatiques
- ✅ Filtrage et recherche
- ✅ Gestion d'erreurs
- ✅ Codes de statut HTTP appropriés
- ✅ Documentation automatique

## 📡 Endpoints disponibles

### Cours (avec filtrage)
```
GET    /api/courses/                    # Liste tous les cours
POST   /api/courses/                    # Créer un cours
GET    /api/courses/{id}/               # Récupérer un cours
PUT    /api/courses/{id}/               # Modifier un cours
DELETE /api/courses/{id}/               # Supprimer un cours
GET    /api/courses/?instructor=Dr.%20sara  # Filtrer par instructeur
GET    /api/courses/?search=Python      # Recherche textuelle
```

### Inscriptions
```
GET    /api/studentcourses/             # Liste toutes les inscriptions
POST   /api/studentcourses/             # Créer une inscription
GET    /api/studentcourses/{id}/       # Récupérer une inscription
PUT    /api/studentcourses/{id}/        # Modifier une inscription
DELETE /api/studentcourses/{id}/        # Supprimer une inscription
GET    /api/studentcourses/by_student/?student_id=123  # Cours d'un étudiant
```

### Validation des étudiants
```
GET    /api/students/validate/{id}/     # Valider un étudiant
```

### Routes fonctionnelles (sans filtrage)
```
POST   /api/courses/add/                # Créer un cours
GET    /api/courses/                    # Liste tous les cours
GET    /api/courses/{id}/               # Récupérer un cours
PUT    /api/courses/update/{id}/        # Modifier un cours
DELETE /api/courses/delete/{id}/        # Supprimer un cours
POST   /api/studentcourse/add/          # Inscrire un étudiant
```

## 🔧 Configuration requise

### Packages Python
```bash
pip install django
pip install djangorestframework
pip install django-filter
pip install requests
```

### Configuration Spring Boot
Le microservice Student Service doit exposer :
```
GET /api/students/{id}
```

## 🚀 Démarrage du projet

1. **Installer les dépendances** :
   ```bash
   pip install django djangorestframework django-filter requests
   ```

2. **Appliquer les migrations** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

4. **Démarrer le microservice Spring Boot** sur le port 8080

## 🧪 Tests avec Postman

### Créer un cours
```json
POST http://localhost:8000/api/courses/
{
    "name": "Python Programming",
    "instructor": "Dr. Sara",
    "category": "Programming",
    "schedule": "Lundi 9h-11h"
}
```

### Filtrer les cours
```
GET http://localhost:8000/api/courses/?instructor=Dr.%20sara
GET http://localhost:8000/api/courses/?search=Python
```

### Inscrire un étudiant
```json
POST http://localhost:8000/api/studentcourse/add/
{
    "student_id": 123,
    "course": 1
}
```

### Valider un étudiant
```
GET http://localhost:8000/api/students/validate/123/
```

## 📊 Gestion des erreurs

### Erreurs de validation
- **400 Bad Request** : Données invalides
- **404 Not Found** : Ressource non trouvée
- **500 Internal Server Error** : Erreur serveur

### Erreurs microservice
- **Timeout** : Service non disponible
- **Connection Error** : Impossible de se connecter
- **Student Not Found** : Étudiant inexistant

## 🔒 Sécurité

### Développement
- DEBUG = True (désactiver en production)
- SECRET_KEY exposée (changer en production)
- ALLOWED_HOSTS vide (configurer en production)

### Production recommandée
- HTTPS obligatoire
- Authentification entre services
- Validation des données d'entrée
- Rate limiting
- Logs de sécurité

## 📈 Améliorations possibles

1. **Authentification** : JWT, OAuth2
2. **Cache** : Redis pour les appels microservice
3. **Monitoring** : Logs, métriques, alertes
4. **Tests** : Tests unitaires et d'intégration
5. **Documentation** : Swagger/OpenAPI
6. **Déploiement** : Docker, Kubernetes

## 🎓 Points d'apprentissage

### Django REST Framework
- **ViewSets** : Opérations CRUD automatiques
- **Serializers** : Conversion JSON ↔ Objets
- **Filtrage** : DjangoFilterBackend, SearchFilter
- **Pagination** : Gestion des grandes listes

### Architecture microservices
- **Communication HTTP** : Requests, timeouts, erreurs
- **Validation externe** : Appels vers services tiers
- **Gestion d'erreurs** : Fallback, retry, circuit breaker
- **Logging** : Traçabilité des appels

### Bonnes pratiques
- **Séparation des responsabilités** : Models, Views, Services
- **Configuration** : Settings centralisés
- **Documentation** : Commentaires détaillés
- **Gestion d'erreurs** : Codes HTTP appropriés
