from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse_email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    clef_securite = models.CharField(max_length=100)

class OffreDeBillets(models.Model):
    TYPES_CHOICES = [
        ('Solo', 'Solo'),
        ('Duo', 'Duo'),
        ('Familiale', 'Familiale'),
    ]
    type = models.CharField(max_length=50, choices=TYPES_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_ventes = models.IntegerField(default=0)

class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    offre_de_billets = models.ForeignKey(OffreDeBillets, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    offre_de_billets = models.ForeignKey(OffreDeBillets, on_delete=models.CASCADE)
    clef_securite_1 = models.CharField(max_length=100)
    clef_securite_2 = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/')

class Administrateur(models.Model):
    nom_utilisateur = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)
