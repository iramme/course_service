


# Ce fichier contient toutes les fonctions et classes qui gèrent les requêtes HTTP
# Il définit comment l'API répond aux différentes requêtes (GET, POST, PUT, DELETE)

#
from django_filters.rest_framework import DjangoFilterBackend  # Pour le filtrage exact des données
import requests
from django.db.models import Q
from rest_framework import viewsets, filters  # Viewsets pour les opérations CRUD automatiques
from rest_framework.decorators import action  # Pour créer des routes personnalisées dans les viewsets
from rest_framework.response import Response  # Pour envoyer des réponses HTTP au format JSON
from rest_framework.decorators import api_view  # Décorateur pour les vues basées sur des fonctions
from rest_framework import status  # Constantes pour les codes de statut HTTP (200, 404, 201, etc.)

from .models import Course, StudentCourse  # Importation des modèles (tables de la base de données)
from .serializers import CourseSerializer, StudentCourseSerializer  # Sérialiseurs pour convertir les objets en JSON
from .services import student_service  # Service pour communiquer avec le microservice Student Service  

# Ces fonctions gèrent les opérations CRUD (Create, Read, Update, Delete) pour les cours
# Chaque fonction correspond à une route HTTP spécifique
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
# CRÉER UN COURS (POST)
@api_view(['POST'])  # Décorateur qui spécifie que cette fonction accepte seulement les requêtes POST
def add_course(request):
    """
    Fonction pour créer un nouveau cours
    
    URL: POST /api/courses/add/
    Body JSON: {"name": "Python", "instructor": "Dr. Sara", "category": "Programming", "schedule": "Lundi 9h-11h"}
    """
    # Créer un sérialiseur avec les données reçues du client (Postman, frontend, etc.)
    serializer = CourseSerializer(data=request.data)
    
    # Vérifier si les données sont valides (tous les champs requis sont présents, formats corrects)
    if serializer.is_valid():
        # Sauvegarder le cours dans la base de données
        serializer.save()
        # Retourner une réponse de succès avec le code 201 (Created)
        return Response(
            {"message": "✅ Course added successfully!"}, 
            status=status.HTTP_201_CREATED
        )
    else:
        # Si les données ne sont pas valides, retourner les erreurs avec le code 400 (Bad Request)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )



# RÉCUPÉRER TOUS LES COURS (GET)

@api_view(['GET'])  # Décorateur qui spécifie que cette fonction accepte seulement les requêtes GET
def get_all_courses(request):
    """
    Fonction pour récupérer tous les cours
    
    URL: GET /api/courses/
    """
    # Récupérer tous les cours depuis la base de données
    courses = Course.objects.all()
    
    # Convertir les objets Course en format JSON (many=True car on a plusieurs objets)
    serializer = CourseSerializer(courses, many=True)
    
    # Retourner la liste des cours au client
    return Response(serializer.data)

# RÉCUPÉRER UN COURS PAR SON ID (GET)

@api_view(['GET'])
def get_course_by_id(request, pk):  # pk = primary key (identifiant unique du cours)
    """
    Fonction pour récupérer un cours spécifique par son ID
    
    URL: GET /api/courses/{id}/
    """
    try:
        # Rechercher le cours par son ID dans la base de données
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist: 
        # Si le cours n'existe pas, retourner une erreur 404 (Not Found)
        return Response(
            {"error": "❌ Course not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Convertir l'objet Course en format JSON
    serializer = CourseSerializer(course)
    
    # Retourner les données du cours
    return Response(serializer.data)


# MODIFIER UN COURS (PUT)
@api_view(['PUT'])
def update_course(request, pk):
    """
    Fonction pour modifier un cours existant
    
    URL: PUT /api/courses/update/{id}/
    Body JSON: {"name": "Python Advanced", "instructor": "Dr. Sara", ...}
    """
    try:
        # Récupérer le cours à modifier
        course = Course.objects.get(pk=pk) 
    except Course.DoesNotExist: 
        # Si le cours n'existe pas, retourner une erreur 404
        return Response(
            {"error": "❌ Course not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Créer un sérialiseur avec le cours existant et les nouvelles données
    # Le paramètre 'data' contient les nouvelles données à appliquer
    serializer = CourseSerializer(course, data=request.data)
    
    # Vérifier si les nouvelles données sont valides
    if serializer.is_valid():  
        # Sauvegarder les modifications dans la base de données
        serializer.save()
        # Retourner un message de succès
        return Response({"message": "✅ Course updated successfully"})
    else:
        # Si les données ne sont pas valides, retourner les erreurs
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

# SUPPRIMER UN COURS (DELETE)
@api_view(['DELETE'])
def delete_course(request, pk):
    """
    Fonction pour supprimer un cours
    
    URL: DELETE /api/courses/delete/{id}/
    """
    try:
        # Récupérer le cours à supprimer
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        # Si le cours n'existe pas, retourner une erreur 404
        return Response(
            {"error": "❌ Course not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Supprimer le cours de la base de données
    course.delete()
    
    # Retourner un message de confirmation
    return Response({"message": "🗑️ Course deleted successfully"})
# en haut du fichier (ajoute cet import si pas déjà présent)


# ... puis la fonction corrigée :
@api_view(['GET'])
def search_courses(request):
    """
    Recherche par paramètre(s) :
      - /api/courses/search/?q=Python
      - http://127.0.0.1:8000/api/courses/search/?name=Python
      - /api/courses/search/?instructor=Sara
      - http://127.0.0.1:8000/api/courses/search/?category=Programmation
      - Combinaisons possibles
    """
    q = request.GET.get('q', '').strip()
    name = request.GET.get('name', '').strip()
    instructor = request.GET.get('instructor', '').strip()
    category = request.GET.get('category', '').strip()

    # Si aucun paramètre donné, renvoyer erreur (plutôt que tout)
    if not (q or name or instructor or category):
        return Response(
            {"detail": "Fournir au moins un paramètre de recherche: q, name, instructor ou category."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Construire la requête dynamiquement avec Q()
    filters = Q()  # <-- utiliser Q(), pas q()
    if q:
        filters &= (Q(name__icontains=q) | Q(instructor__icontains=q) | Q(category__icontains=q))
    if name:
        filters &= Q(name__icontains=name)
    if instructor:
        filters &= Q(instructor__icontains=instructor)
    if category:
        filters &= Q(category__icontains=category)

    results = Course.objects.filter(filters).distinct()

    if not results.exists():
        return Response({"message": "Aucun cours trouvé."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(results, many=True)
    return Response(serializer.data)
# ===============================================================
# INSCRIPTION D'UN ÉTUDIANT À UN COURS
# ===============================================================

@api_view(['POST'])
def enroll_student(request):
    """
    Inscrire un étudiant à un cours.
    Exemple : POST /api/enroll/
    Body JSON :
    {
        "student_id": 1,
        "course_id": 3
    }
    """
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    # 1️⃣ Vérification des champs obligatoires
    if not student_id or not course_id:
        return Response(
            {"error": "Les champs 'student_id' et 'course_id' sont requis."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2️⃣ Vérifier si le cours existe
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(
            {"error": "Cours introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3️⃣ Vérifier si l'étudiant existe dans le Student Service
    try:
        student_response = requests.get(f"https://student-service-1.onrender.com/api/students/{student_id}")
        if student_response.status_code != 200:
            return Response(
                {"error": "Étudiant introuvable dans le service Student."},
                status=status.HTTP_404_NOT_FOUND
            )
    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Erreur de connexion au Student Service : {str(e)}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # 4️⃣ Vérifier si l'étudiant est déjà inscrit
    existing = StudentCourse.objects.filter(student_id=student_id, course=course).first()
    if existing:
        return Response(
            {"message": "⚠️ L'étudiant est déjà inscrit à ce cours."},
            status=status.HTTP_200_OK
        )

    # 5️⃣ Créer l'inscription
    StudentCourse.objects.create(student_id=student_id, course=course)
    return Response(
        {"message": "✅ Étudiant inscrit avec succès."},
        status=status.HTTP_201_CREATED
    )
# ===============================================================
# LISTER LES COURS D'UN ÉTUDIANT
# ===============================================================
# ===============================================================
# LISTER LES ÉTUDIANTS D'UN COURS
# ===============================================================

@api_view(['GET'])
def get_students_by_course(request, course_id):
    """
    Récupérer tous les étudiants inscrits à un cours.
    Exemple : GET /api/course/1/students/
    """
    try:
        # Vérifier si le cours existe
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(
            {"error": "❌ Cours introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Récupérer toutes les inscriptions pour ce cours
    enrollments = StudentCourse.objects.filter(course=course)
    
    students_data = []
    
    # Pour chaque inscription, récupérer les détails de l'étudiant
    for enrollment in enrollments:
        try:
            # Appeler le Student Service pour récupérer les infos complètes
            student_response = requests.get(f"https://student-service-1.onrender.com/api/students/{enrollment.student_id}")
            
            if student_response.status_code == 200:
                student_data = student_response.json()
                students_data.append({
                    "id": student_data.get("id"),
                    "first_name": student_data.get("firstName", ""),
                    "last_name": student_data.get("lastName", ""),
                    "email": student_data.get("email", ""),
                    # Ajouter d'autres champs si nécessaire
                })
            else:
                # Si l'étudiant n'est pas trouvé, utiliser les infos de base
                students_data.append({
                    "id": enrollment.student_id,
                    "first_name": "Étudiant",
                    "last_name": f"#{enrollment.student_id}",
                    "email": "Non disponible"
                })
                
        except requests.exceptions.RequestException as e:
            # En cas d'erreur de connexion
            students_data.append({
                "id": enrollment.student_id,
                "first_name": "Étudiant",
                "last_name": f"#{enrollment.student_id}",
                "email": "Service indisponible"
            })

    return Response({
        "course_id": course_id,
        "course_name": course.name,
        "students": students_data
    })
@api_view(['GET'])
def get_courses_by_student(request, student_id):
    """
    Récupérer tous les cours d’un étudiant.
    Exemple : GET /api/student/1/courses/
    """
    enrollments = StudentCourse.objects.filter(student_id=student_id)
    courses = [en.course for en in enrollments]
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
   