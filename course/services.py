# =============================================================================
# SERVICE DE COMMUNICATION MICROSERVICE (course/services.py)
# =============================================================================
# Ce fichier contient la logique pour communiquer avec le microservice Student Service
# Il gère les appels HTTP vers le service Spring Boot et la gestion des erreurs

# =============================================================================
# IMPORTS
# =============================================================================
import requests  # Bibliothèque pour faire des appels HTTP
# Bibliothèque pour faire des appels HTTP
import logging  # Pour enregistrer les logs (erreurs, informations)
from django.conf import settings  # Pour accéder aux paramètres de configuration Django

# Configuration du système de logging
# Cela permet d'enregistrer les erreurs et informations dans les logs Django
logger = logging.getLogger(__name__)


# =============================================================================
# CLASSE STUDENTSERVICE - Communication avec le microservice
# =============================================================================
class StudentService:
    """
    Service pour communiquer avec le microservice Student Service (Spring Boot)
    
    Cette classe encapsule toute la logique de communication avec le service externe :
    - Configuration des URLs et timeouts
    - Gestion des erreurs de communication
    - Formatage des réponses
    - Logging des opérations
    """
    
    def __init__(self):
        """
        Constructeur de la classe StudentService
        
        Initialise les paramètres de configuration depuis les settings Django
        """
        # Récupérer l'URL de base du microservice depuis les settings
        # Si STUDENT_SERVICE_URL n'est pas défini, utiliser la valeur par défaut
        self.base_url = getattr(
            settings, 
            'STUDENT_SERVICE_URL', 
            'http://localhost:8081/api/students'
        )
        
        # Récupérer le timeout pour les appels HTTP depuis les settings
        # Si STUDENT_SERVICE_TIMEOUT n'est pas défini, utiliser 5 secondes
        self.timeout = getattr(
            settings, 
            'STUDENT_SERVICE_TIMEOUT', 
            5
        )
    
    def get_student_by_id(self, student_id):
        """
        Récupère un étudiant par son ID depuis le microservice Student Service
        
        Args:
            student_id (int): ID de l'étudiant à récupérer
            
        Returns:
            dict: Dictionnaire contenant :
                - success (bool): True si l'opération a réussi
                - data (dict): Données de l'étudiant si succès
                - error (str): Message d'erreur si échec
                - student_id (int): ID de l'étudiant demandé
        """
        try:
            # Construire l'URL complète pour récupérer l'étudiant
            # Exemple: http://localhost:8080/api/students/123
            url = f"{self.base_url}/{student_id}"
            
            # Faire l'appel HTTP GET vers le microservice
            # timeout=self.timeout : arrêter l'appel après X secondes
            response = requests.get(url, timeout=self.timeout)
            
            # Analyser le code de statut de la réponse HTTP
            if response.status_code == 200:
                # Succès : l'étudiant existe
                return {
                    'success': True,
                    'data': response.json(),  # Convertir la réponse JSON en dictionnaire Python
                    'student_id': student_id
                }
            elif response.status_code == 404:
                # L'étudiant n'existe pas
                return {
                    'success': False,
                    'error': 'Student not found',
                    'student_id': student_id
                }
            else:
                # Autre erreur du serveur (500, 503, etc.)
                return {
                    'success': False,
                    'error': f'Student service error: {response.status_code}',
                    'student_id': student_id
                }
                
        except requests.exceptions.Timeout:
            # Le microservice ne répond pas dans le délai imparti
            logger.error(f"Timeout when calling student service for student {student_id}")
            return {
                'success': False,
                'error': 'Student service timeout',
                'student_id': student_id
            }
        except requests.exceptions.ConnectionError:
            # Impossible de se connecter au microservice (service arrêté, URL incorrecte)
            logger.error(f"Connection error when calling student service for student {student_id}")
            return {
                'success': False,
                'error': 'Student service unavailable',
                'student_id': student_id
            }
        except Exception as e:
            # Toute autre erreur inattendue
            logger.error(f"Unexpected error when calling student service for student {student_id}: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'student_id': student_id
            }
    
    def validate_students(self, student_ids):
        """
        Valide plusieurs étudiants en une seule fois
        
        Args:
            student_ids (list): Liste des IDs d'étudiants à valider
            
        Returns:
            list: Liste de dictionnaires contenant les résultats pour chaque étudiant
        """
        results = []
        # Parcourir chaque ID d'étudiant
        for student_id in student_ids:
            # Valider chaque étudiant individuellement
            result = self.get_student_by_id(student_id)
            results.append(result)
        return results
    
    def is_student_valid(self, student_id):
        """
        Vérifie rapidement si un étudiant existe (retourne True/False)
        
        Args:
            student_id (int): ID de l'étudiant à vérifier
            
        Returns:
            bool: True si l'étudiant existe, False sinon
        """
        # Faire l'appel au microservice
        result = self.get_student_by_id(student_id)
        # Retourner seulement le statut de succès
        return result['success']


# =============================================================================
# INSTANCE GLOBALE DU SERVICE
# =============================================================================
# Créer une instance unique du service qui sera utilisée dans toute l'application
# Cela évite de recréer l'objet à chaque appel
student_service = StudentService()
