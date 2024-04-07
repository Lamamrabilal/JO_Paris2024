
import hashlib
from pickle import FALSE
from django.utils import timezone
import uuid
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models


class GestionnaireUtilisateur(BaseUserManager):
    def create_user(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'email doit être spécifié")
        adresse_email = self.normalize_email(email)
        utilisateur = self.model(email=adresse_email, nom=nom,
                                 prenom=prenom, **extra_fields)
        utilisateur.set_password(mot_de_passe)
        utilisateur.save(using=self._db)
        return utilisateur


    def create_superuser(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields['is_staff']:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if not extra_fields['is_superuser']:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, nom, prenom, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    is_actif = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    clef_1 = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    objects = GestionnaireUtilisateur()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def generer_cle(self):
        self.clef = uuid.uuid4()
        self.save()
  

class OffreDeBillet(models.Model):
    TYPES_CHOICES = [
        ('Solo', 'Solo'),
        ('Duo', 'Duo'),
        ('Familiale', 'Familiale'),
    ]
    type = models.CharField(max_length=50, choices=TYPES_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_ventes = models.IntegerField(default=0)

    @classmethod
    def creer_offre(cls, type, description, prix):
        return cls.objects.create(type=type, description=description, prix=prix)

    def modifier_offre(self, offre_id, **kwargs):
        offre = self.objects.get(pk=offre_id)
        for attr, value in kwargs.items():
            setattr(offre, attr, value)
        offre.save()
        return offre

    @classmethod
    def lister_offres(cls):
        return cls.objects.all()

    @classmethod
    def ajouter_nouveaux_choix(cls, nouveaux_choix):
        for choix in nouveaux_choix:
            cls.TYPES_CHOICES.append(choix)
        cls._meta.get_field('type').choices = cls.TYPES_CHOICES

    def ajouter_utilisateurs(self, nombre_utilisateurs):
        if self.type == 'Duo':
            nombre_utilisateurs_a_ajouter = 2 * nombre_utilisateurs
        elif self.type == 'Familiale':
            nombre_utilisateurs_a_ajouter = 4 * nombre_utilisateurs
        else:
            nombre_utilisateurs_a_ajouter = nombre_utilisateurs

        for _ in range(nombre_utilisateurs_a_ajouter):
            utilisateur = Utilisateur.objects.create(
                username=f"utilisateur_{Utilisateur.objects.count() + 1}")


    def __str__(self):
        return f"{self.type}"


class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    offre_de_billets = models.ForeignKey(
        OffreDeBillet, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    clef_2 = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.utilisateur}"

    def generer_cle(self):
        self.clef = uuid.uuid4()
        self.save()


class Ticket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    offre_de_billets = models.ForeignKey(
        OffreDeBillet, on_delete=models.CASCADE)
    clef_finale = models.CharField(
        max_length=100, editable=False, default='default_value')
    qr_code = models.ImageField(upload_to='qr_codes/')

    def generer_cle_finale(self):
        # Concaténation des clés des utilisateurs et des réservations
        clef_concatenee = f"{self.reservation.utilisateur.clef_1}-{self.reservation.clef_2}"

        # Utilisation de la concaténation des clés pour créer une clé finale sécurisée
        self.clef_finale = hashlib.sha256(clef_concatenee.encode()).hexdigest()

    def generer_e_billet(self):

        self.generer_cle_finale()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.clef_finale)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')

        file_name = f"e_billet_{self.id}.png"
        self.qr_code.save(file_name, InMemoryUploadedFile(
            buffer, None, file_name, 'image/png', buffer.tell, None))

        self.save()
