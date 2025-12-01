FROM python:3.11-slim
WORKDIR /app
# Copier le fichier des dépendances
COPY requirements.txt .
# Installer les dépendances et gunicorn (version compatible)
RUN pip install --upgrade pip && pip install -r requirements.txt
# Copier le reste du code
COPY . .
# Exposer le port
EXPOSE 8000
# Commande pour lancer l'application
CMD ["gunicorn", "course_service.wsgi:application", "--bind", "0.0.0.0:8000"]
