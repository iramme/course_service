# =============================================================================
# SÉRIALISEURS (course/serializers.py)
# =============================================================================
# Ce fichier définit comment convertir les objets Python (modèles) en JSON
# et vice versa. Les sérialiseurs sont essentiels pour l'API REST.

# =============================================================================
# IMPORTS
# =============================================================================
from rest_framework import serializers  # Classes de base pour créer des sérialiseurs
from .models import Course, StudentCourse  # Importation des modèles à sérialiser

# =============================================================================
# SÉRIALISEUR POUR LES COURS
# =============================================================================
class CourseSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Course
    
    Ce sérialiseur convertit :
    - Objet Course → JSON (pour les réponses API)
    - JSON → Objet Course (pour créer/modifier des cours)
    
    Exemple de JSON généré :
    {
        "id": 1,
        "name": "Python Programming",
        "instructor": "Dr. Sara",
        "category": "Programming",
        "schedule": "Lundi 9h-11h"
    }
    """
    
    class Meta:
        """
        Classe Meta pour configurer le sérialiseur
        """
        model = Course  # Modèle à sérialiser
        fields = '__all__'  # Inclure automatiquement tous les champs du modèle
        
        # Champs inclus automatiquement :
        # - id : Identifiant unique du cours (généré automatiquement par Django)
        # - name : Nom du cours
        # - instructor : Nom de l'instructeur
        # - category : Catégorie du cours
        # - schedule : Horaire du cours


# =============================================================================
# SÉRIALISEUR POUR LES INSCRIPTIONS ÉTUDIANT-COURS
# =============================================================================
class StudentCourseSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle StudentCourse
    
    Ce sérialiseur convertit :
    - Objet StudentCourse → JSON (pour les réponses API)
    - JSON → Objet StudentCourse (pour créer des inscriptions)
    
    Exemple de JSON généré :
    {
        "id": 1,
        "student_id": 123,
        "course": 1,
        "course_name": "Python Programming"
    }
    """
    
    # Champ calculé : récupère le nom du cours depuis la relation ForeignKey
    # source='course.name' : va chercher le champ 'name' de l'objet 'course' lié
    # read_only=True : ce champ ne peut pas être modifié directement
    course_name = serializers.CharField(
        source='course.name', 
        read_only=True
    )
    
    class Meta:
        """
        Classe Meta pour configurer le sérialiseur
        """
        model = StudentCourse  # Modèle à sérialiser
        fields = ['id', 'student_id', 'course', 'course_name']  # Champs à inclure dans le JSON
        
        # Champs inclus :
        # - id : Identifiant unique de l'inscription
        # - student_id : ID de l'étudiant (vient du microservice Student Service)
        # - course : ID du cours (clé étrangère vers Course)
        # - course_name : Nom du cours (champ calculé, lecture seule)
