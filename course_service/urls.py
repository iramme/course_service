from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # Routes de ton application principale "course"
    # Exemple :
    #   GET  /api/courses/
    #   GET  /api/studentcourses/
    #   GET  /api/studentcourses/by_student/?student_id=1
    path('api/', include('course.urls')),

    # Optionnel : page d'accueil simple (pour vérifier que le serveur tourne)
    path('', lambda request: HttpResponse("✅ Course Service is running.")),
]
