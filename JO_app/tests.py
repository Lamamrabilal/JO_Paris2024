from django.test import TestCase
from .models import Utilisateur, OffreDeBillet, Reservation, Ticket
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UtilisateurTestCase(TestCase):
    def test_creation_utilisateur(self):
       
        email = "test@example.com"
        nom = "Doe"
        prenom = "John"
        mot_de_passe = "testpassword"

        utilisateur = Utilisateur.objects.create_user(
            email=email,
            nom=nom,
            prenom=prenom,
            mot_de_passe=mot_de_passe
        )

      
        self.assertEqual(utilisateur.email, email)
        self.assertEqual(utilisateur.nom, nom)
        self.assertEqual(utilisateur.prenom, prenom)
        self.assertTrue(utilisateur.check_password(mot_de_passe))
        self.assertTrue(utilisateur.is_active)
        self.assertFalse(utilisateur.is_staff)
        self.assertTrue(Utilisateur.objects.filter(email=email).exists())

    def test_create_superuser(self):
       
        email = "admin@example.com"
        nom = "Admin"
        prenom = "User"
        mot_de_passe = "password"
        extra_fields = {}

        
        superuser = Utilisateur.objects.create_superuser(
            email=email,
            nom=nom,
            prenom=prenom,
            mot_de_passe=mot_de_passe,
            **extra_fields
        )

        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.nom, nom)
        self.assertEqual(superuser.prenom, prenom)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        
     
class OffreDeBilletTestCase(TestCase):
    def test_creer_offre(self):
        offre = OffreDeBillet.creer_offre(
            type='Solo', description='Billet individuel', prix=10.00)
        self.assertEqual(offre.type, 'Solo')
        self.assertEqual(offre.description, 'Billet individuel')
        self.assertEqual(offre.prix, 10.00)

    def test_ajouter_nouveaux_choix(self):
        OffreDeBillet.ajouter_nouveaux_choix(
            [('Groupe', 'Groupe'), ('VIP', 'VIP')])
        self.assertIn(('Groupe', 'Groupe'), OffreDeBillet.TYPES_CHOICES)
        self.assertIn(('VIP', 'VIP'), OffreDeBillet.TYPES_CHOICES)


class ReservationTestCase(TestCase):
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email='test@example.com', nom='Doe', prenom='John', mot_de_passe='test123')
        self.offre = OffreDeBillet.creer_offre(
            type='Solo', description='Billet individuel', prix=10.00)

    def test_creer_reservation(self):
        reservation = Reservation.objects.create(
            utilisateur=self.utilisateur, offre_de_billets=self.offre)
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.utilisateur, self.utilisateur)
        self.assertEqual(reservation.offre_de_billets, self.offre)

  


class TicketTestCase(TestCase):
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email='test@example.com', nom='Doe', prenom='John', mot_de_passe='test123')
        self.offre = OffreDeBillet.creer_offre(
            type='Solo', description='Billet individuel', prix=10.00)
        self.reservation = Reservation.objects.create(
            utilisateur=self.utilisateur, offre_de_billets=self.offre)

    def test_generer_cle_finale(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation, offre_de_billets=self.offre)
        ticket.generer_cle_finale()
        self.assertIsNotNone(ticket.clef_finale)

    def test_generer_e_billet(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation, offre_de_billets=self.offre)
        ticket.generer_e_billet()
        self.assertIsNotNone(ticket.qr_code)
