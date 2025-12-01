from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# --- URLS MANUELLES (fonctions spécifiques) ---
urlpatterns = [
 
    # CRUD via fonctions (optionnel si tu veux garder les endpoints classiques)
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/update/<int:pk>/', views.update_course, name='update_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('courses/<int:pk>/', views.get_course_by_id, name='get_course_by_id'),
    path('courses/', views.get_all_courses, name='get_all_courses'),
    path('courses/search/', views.search_courses, name='search_courses'),
    path('course/<int:course_id>/students/', views.get_students_by_course, name='get_students_by_course'),

# 🔽 Nouvelles routes pour les inscriptions
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('student/<int:student_id>/courses/', views.get_courses_by_student, name='get_courses_by_student'),
]