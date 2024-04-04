from xml.dom import ValidationErr
from django.test import TestCase
from .models import Utilisateur, OffreDeBillet, Reservation, Ticket


class UtilisateurTestCase(TestCase):
    def test_creer_utilisateur(self):
        utilisateur = Utilisateur.objects.create_user(
            email='test@example.com', nom='Doe', prenom='John', mot_de_passe='test123')
        self.assertTrue(utilisateur.email)
        self.assertEqual(utilisateur.nom, 'Doe')
        self.assertEqual(utilisateur.prenom, 'John')
        self.assertTrue(utilisateur.check_password('test123'))

    def test_creer_superutilisateur(self):
        super_utilisateur = Utilisateur.objects.create_superuser(
            email='admin@example.com', nom='Admin', prenom='Super', mot_de_passe='adminpassword')
        self.assertTrue(super_utilisateur.is_staff)
        self.assertTrue(super_utilisateur.is_superuser)


class OffreDeBilletTestCase(TestCase):
    def test_creer_offre(self):
        offre = OffreDeBillet.creer_offre(
            type='Solo', description='Billet individuel', prix=10.00)
       
        self.assertEqual(offre.type, 'Duo')
        self.assertEqual(offre.description, 'Billet individuel')
        self.assertEqual(offre.prix, 10.00)

    def test_ajouter_nouveaux_choix(self):
        OffreDeBillet.ajouter_nouveaux_choix(
            [('Groupe', 'Groupe'), ('VIP', 'VIP')])
       
        self.assertNotIn(('Groupe', 'Groupe'), OffreDeBillet.TYPES_CHOICES)
        self.assertIn(('VIP', 'VIP'), OffreDeBillet.TYPES_CHOICES)





class ReservationTestCase(TestCase):
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email='test@example.com', nom='Doe', prenom='John', mot_de_passe='test123')
  
        self.offre = OffreDeBillet.creer_offre(
            type='Solo', description='Billet individuel', prix=10.00, nombre_de_billets=1)

    def test_creer_reservation(self):
        
        reservation = Reservation.objects.create(
            utilisateur=self.utilisateur, offre_de_billets=self.offre)

       
        self.assertIsNotNone(reservation)

        self.assertEqual(reservation.utilisateur, self.utilisateur)
        self.assertEqual(reservation.offre_de_billets, self.offre)

        with self.assertRaises(ValidationErr):
            Reservation.objects.create(
                utilisateur=self.utilisateur, offre_de_billets=self.offre)


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
       
        self.assertIsNone(ticket.clef_finale)

    def test_generer_e_billet(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation, offre_de_billets=self.offre)
        ticket.generer_e_billet()
   
        self.assertIsNone(ticket.qr_code)
