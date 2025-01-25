
FROM python:3.12-slim

# Empêche Python de générer des fichiers .pyc et désactive le buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Définit le répertoire de travail
WORKDIR /app

# Installe les outils de base nécessaires pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie le fichier requirements.txt et installe les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du projet dans l'image
COPY . /app

# Expose le port 8000 pour Gunicorn
EXPOSE 8000

# Commande par défaut pour démarrer Gunicorn
CMD ["gunicorn", "Jeux_Paris2024.wsgi:application", "--bind", "0.0.0.0:8000"]
