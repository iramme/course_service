# =============================================================================
# MODÈLES DE DONNÉES (course/models.py)
# =============================================================================
# Ce fichier définit la structure des tables de la base de données
# Chaque classe représente une table et chaque attribut représente une colonne

from django.db import models  # Import des classes pour créer les modèles Django

# =============================================================================
# MODÈLE COURSE - Table des cours
# =============================================================================
class Course(models.Model):
    """
    Modèle représentant un cours dans le système
    
    Cette classe crée une table 'course_course' dans la base de données
    avec les colonnes définies ci-dessous
    """
    
    # CharField = Champ de texte avec une longueur maximale
    name = models.CharField(
        max_length=100,  # Longueur maximale du nom du cours
        help_text="Nom du cours (ex: Python Programming)"  # Texte d'aide pour l'admin Django
    )    
    instructor = models.CharField(
        max_length=100,  # Longueur maximale du nom de l'instructeur
        help_text="Nom de l'instructeur (ex: Dr. Sara)"
    )
    category = models.CharField(
        max_length=100,  # Longueur maximale de la catégorie
        help_text="Catégorie du cours (ex: Programmation, Mathématiques)"
    )
    schedule = models.CharField(
        max_length=100,  # Longueur maximale de l'horaire
        help_text="Horaire du cours (ex: Lundi 9h-11h)"
    )
    
    def __str__(self):
        """
        Méthode spéciale qui définit comment afficher l'objet Course
        Quand on fait print(course) ou qu'on affiche dans l'admin Django,
        cela retourne le nom du cours
        """
        return self.name  # Retourne le nom du cours (ex: "Python Programming")
    
    class Meta:
        """
        Classe Meta pour définir des métadonnées sur le modèle
        """
        verbose_name = "Cours"  # Nom singulier affiché dans l'admin Django
        verbose_name_plural = "Cours"  # Nom pluriel affiché dans l'admin Django


# =============================================================================
# MODÈLE STUDENTCOURSE - Table de liaison entre étudiants et cours
# =============================================================================
class StudentCourse(models.Model):
    """
    Modèle représentant l'inscription d'un étudiant à un cours
    
    Cette classe crée une table 'course_studentcourse' dans la base de données
    C'est une table de liaison (many-to-many) entre étudiants et cours
    """
    
    # IntegerField = Champ pour stocker un nombre entier
    # Ici on stocke l'ID de l'étudiant (qui vient du microservice Student Service)
    student_id = models.IntegerField(
        help_text="ID de l'étudiant (vient du microservice Student Service)"
    )
    
    # ForeignKey = Clé étrangère qui lie à un autre modèle
    # on_delete=models.CASCADE = Si le cours est supprimé, supprimer aussi l'inscription
    course = models.ForeignKey(
        Course,  # Modèle vers lequel on fait référence (Course)
        on_delete=models.CASCADE,  # Action à effectuer si le cours est supprimé
        help_text="Cours auquel l'étudiant est inscrit"
    )
    
    def __str__(self):
        """
        Méthode spéciale qui définit comment afficher l'objet StudentCourse
        Retourne une chaîne formatée avec l'ID de l'étudiant et le nom du cours
        """
        return f"Student {self.student_id} - {self.course.name}"
    
    class Meta:
        """
        Classe Meta pour définir des métadonnées sur le modèle
        """
        verbose_name = "Inscription Étudiant-Cours"  # Nom singulier
        verbose_name_plural = "Inscriptions Étudiant-Cours"  # Nom pluriel
        # unique_together = Contrainte d'unicité : un étudiant ne peut s'inscrire qu'une fois à un cours
        unique_together = ('student_id', 'course')
