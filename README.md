Application des Jeux Olympiques Paris 2024
Cette application permet aux utilisateurs de s'inscrire, de se connecter, de consulter les offres de billets pour divers sports, d'ajouter des offres au panier, de procéder au paiement et de télécharger des tickets.
Fonctionnalités
•	Inscription et Connexion : Les utilisateurs peuvent créer un compte et se connecter.
•	Page d'accueil : Présentation des sports et des sites des Jeux Olympiques.
•	Consultation des Offres : Affichage des différentes offres de billets disponibles.
•	Panier : Ajout et suppression d'offres dans le panier.
•	Paiement : Simulation de paiement et création de réservations.
•	Téléchargement de Tickets : Génération et téléchargement de tickets PDF avec QR code.
Installation
Prérequis
•	Python 3.8 ou plus
•	Django 3.2 ou plus
•	Heroku CLI (pour le déploiement)
Étapes
1.	Cloner le dépôt :
bash
Copier le code
git https://github.com/Lamamrabilal/JO_Paris2024.git
cd Lamamrabilal/JO_Paris2024.git
2.	Créer et activer un environnement virtuel :
bash
Copier le code
python -m venv venv
3.	Installer les dépendances :
bash
Copier le code
pip install -r requirements.txt
4.	Configurer la base de données :
•	Modifier les paramètres de base de données dans settings.py.
•	Appliquer les migrations :
bash
Copier le code
python manage.py migrate
5.	Lancer le serveur local :
bash
Copier le code
python manage.py runserver
6.	Créer un superutilisateur (pour accéder à l'admin) :
bash
Copier le code
python manage.py createsuperuser
Déploiement sur Heroku
1.	Connexion à Heroku :
bash
Copier le code
heroku login
2.	Créer une application Heroku :
Bash
Copier le code
heroku create joparis2024
3.	Ajouter les fichiers de configuration pour Heroku :
•	Procfile :
Copier le code :
	 web: gunicorn Jeux_Paris2024.wsgi:application
•	runtime.txt :
Copier le code
python-3.8.10
4.	Pousser sur Heroku :
bash
Copier le code
git push heroku main
5.	Appliquer les migrations sur Heroku :
bash
Copier le code
heroku run python manage.py migrate
6.	Créer un superutilisateur sur Heroku :
bash
Copier le code
heroku run python manage.py createsuperuser
Utilisation
•	Accédez à l'application via l'URL fournie par Heroku.
•	Inscrivez-vous, connectez-vous et explorez les fonctionnalités de l'application.
Contribution
Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour des suggestions d'améliorations.

